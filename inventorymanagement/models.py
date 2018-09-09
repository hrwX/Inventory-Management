from datetime import datetime
from inventorymanagement import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    product = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.user_id)
    
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    product_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_user_id}', '{self.product_quantity}')"

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"'{self.location_name}'"

class LocationInventory(db.Model):
    locationinventory_id = db.Column(db.Integer, primary_key=True)
    locationinventory_product_name = db.Column(db.String(20), nullable=False)

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    from_location_id = db.Column(db.Integer, nullable=False)
    to_location_id = db.Column(db.Integer, nullable=False)
    from_location = db.Column(db.String, nullable=False)
    to_location = db.Column(db.String, nullable=False)
    movement_product_quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"ProductMovement('{self.movement_id}', '{self.from_location}', '{self.to_location}', '{self.movement_product_quantity}', '{self.timestamp}')"
