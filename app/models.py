from app import db

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