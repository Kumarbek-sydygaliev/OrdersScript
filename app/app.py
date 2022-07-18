from flask import Flask, render_template
from turbo_flask import Turbo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from datetime import datetime
import threading
import time

from functions import get_sheet, exchange


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/orderscatalog'

db = SQLAlchemy(app)

from models import *

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


# Auto-Update of database objects
turbo = Turbo(app)
def update_load():
    with app.app_context():
        while True:
            get_orders()
            time.sleep(5)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


# Views
@app.route('/')
def index():
    update_orders()
    return render_template('index.html', orders=Order.query.order_by(desc(Order.date)).all())