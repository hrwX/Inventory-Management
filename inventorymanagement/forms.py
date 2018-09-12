from flask_wtf import FlaskForm
from inventorymanagement import app, mysql, db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField
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
    submit = SubmitField('Add Product')

########################Locations######################################

class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')

########################ProductMovements######################################

class AddProductMovement(FlaskForm):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT location_name FROM location")
    locations = cursor.fetchall()
    values = []
    
    for location in locations:
        values.append((location[0], location[0]))
    
    name = StringField('Product Name', validators=[DataRequired()])
    fromLocation = SelectField('From Location', choices=values, validators=[DataRequired()])   
    toLocation = SelectField('To Location', choices=values, validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    timestamp = DateField('Date', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Move Product')