from flask_wtf import FlaskForm
from inventorymanagement import app, db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, SelectField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from inventorymanagement.models import User, Product, Location, ProductMovement, LocationInventory

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #location = str(Location.query.all())
    #print(location)
    #loc = [('one', 'one'), ('two', 'two')]
    #loc = ([('Mumbai', 'Mumbai'), ('Bangalore', 'Bangalore'), ('Delhi', 'Delhi'), ('Chennai', 'Chennai'), ('Kolkata', 'Kolkata')])
    #yes_no = SelectField('Select option', choices=loc)
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email Taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    locations = Location.query.all()
    for location in locations:
        row_location = (str(location) + "_location").replace("'", "") #mumbai_location
        print("Forms.py" + row_location)
        row_location = IntegerField(''+ str(location) +' Quantity', validators=[DataRequired()])  
    #quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    #location = IntegerField('Product Location', validators=[DataRequired()])

    submit = SubmitField('Add Product')

    def validate_product(self, product):
        product = Product.query.filter_by(product_name = product.data).first()
        if product:
            raise ValidationError('Product Taken')

class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')

class AddProductMovement(FlaskForm):
    locations = Location.query.all()
    values = []
    for location in locations:
        values.append((location.location_name, location.location_name))
    #print(values)
    name = StringField('Product Name', validators=[DataRequired()])
    product_id = IntegerField(validators=[DataRequired()])
    fromLocation = SelectField('From Location', choices=values, validators=[DataRequired()])
    fromLocationId = IntegerField(validators=[DataRequired()])
    toLocation = SelectField('To Location', choices=values, validators=[DataRequired()])
    toLocationId = IntegerField(validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    timestamp = DateTimeField(validators=[DataRequired()])
    submit = SubmitField('Move Product')