from flask_wtf import FlaskForm
from inventorymanagement import app, mysql, db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, SelectField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from inventorymanagement.models import User

########################Users######################################

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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

########################Products######################################

class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    #print(name)        
    #def add(self, locations): #initializing dynamic fields      
    #    for location in locations:
    #        location = StringField(location, validators=[DataRequired()])
    #        print(location)
    submit = SubmitField('Add Product')

    def validate_product(self, product):
        product = Product.query.filter_by(product_name = product.data).first()
        if product:
            raise ValidationError('Product Taken')

########################Locations######################################

class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')
    def validate_location(self, location):
        location = Location.query.filter_by(location_name = location.data).first()
        if location:
            raise ValidationError('Location Present')

########################ProductMovements######################################

class AddProductMovement(FlaskForm):
    locations = ''#Location.query.all()
    values = []
    for location in locations:
        values.append((location.location_name, location.location_name))
    
    name = StringField('Product Name', validators=[DataRequired()])
    product_id = IntegerField(validators=[DataRequired()])
    
    fromLocation = SelectField('From Location', choices=values, validators=[DataRequired()])
    fromLocationId = IntegerField(validators=[DataRequired()])
    
    toLocation = SelectField('To Location', choices=values, validators=[DataRequired()])
    toLocationId = IntegerField(validators=[DataRequired()])
    
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    
    timestamp = DateTimeField(validators=[DataRequired()])
    submit = SubmitField('Move Product')