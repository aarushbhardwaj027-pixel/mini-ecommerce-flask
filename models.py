from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)

    role = db.Column(db.Enum("buyer", "seller", name="user_roles"))
    username = db.Column(db.String(200),unique = True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200),unique=True)

    product = db.relationship('Products',backref = 'author')
    order = db.relationship('Order',backref = 'author')

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)

    product_name = db.Column(db.String(200))
    product_description = db.Column(db.String(600))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)

    user_id = db.Column(db.Integer , db.ForeignKey('users.id'))

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default=False)

    product = db.relationship('Products',backref = 'orders')
    

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))