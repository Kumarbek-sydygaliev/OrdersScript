# import libraries
from flask import Flask
from flask import (
    render_template, request
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

# import functions
from sheets import get_sheet
from currency import exchange


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/orderscatalog'
app.debug = True
db = SQLAlchemy(app)


# models
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


# views
@app.route('/')
def index():
    
    for order in get_sheet():
        order = list(order.values())

        if not Order.query.filter_by(number=order[1]).first():
            order = Order(
                number = order[1],
                price_usd = order[2],
                date = datetime.strptime(order[3], '%d.%m.%Y'),
                price_rub = exchange(order[2])
            )
            
            db.session.add(order)
            db.session.commit()

    
    return render_template('index.html', orders=Order.query.order_by(desc(Order.date)).all())