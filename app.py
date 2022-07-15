from operator import itemgetter
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from turbo_flask import Turbo

from datetime import datetime
from sqlalchemy import desc
import threading
import time

### Import functions
from sheets import get_sheet
from currency import exchange


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/orderscatalog'
app.debug = True
db = SQLAlchemy(app)


### Models
class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    price_usd = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    price_rub = db.Column(db.Integer)
    
    def __init__(self, number, price_usd, date, price_rub):
        self.number = number
        self.price_usd = price_usd
        self.date = date
        self.price_rub = price_rub

db.create_all()


def get_orders():
    orders = get_sheet()
    for order in orders:
        order = list(order.values())
        try:
            item = Order(
                    number = order[1],
                    price_usd = order[2],
                    date = datetime.strptime(order[3], '%d.%m.%Y'),
                    price_rub = exchange(order[2])
            )
            if not Order.query.filter_by(number=order[1]).first():  
                db.session.add(item)
            else:
                Order.query.filter_by(number=item.number).update(dict(
                    number=item.number,
                    price_usd=item.price_usd,
                    date=item.date,
                    price_rub=item.price_rub
                ))
            db.session.commit()
        except Exception as error: # If error occured during session
            db.session.rollback()
            print(datetime.today(), '   ERROR:  ', error.__str__, '\n')
            break

def update_orders():
    numbers_in_sheet = [i['заказ №'] for i in get_sheet()]
    for order in Order.query.all():
        if not order.number in numbers_in_sheet:
            Order.query.filter_by(number=order.number).delete()
    pass


### Auto-Update of database objects
turbo = Turbo(app)
def update_load():
    with app.app_context():
        while True:
            get_orders()
            time.sleep(5)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


### Views
@app.route('/')
def index():
    update_orders()
    return render_template('index.html', orders=Order.query.order_by(desc(Order.date)).all())

if __name__ == '__main__':
    app.run(debug=True, host='localhost')