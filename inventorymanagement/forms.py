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

class ProductMovement(FlaskForm):   
    name = StringField('Product Name', validators=[DataRequired()])   
    #timestamp = DateField('Date', validators=[DataRequired()])
    #fromLocation = SelectField('From Location', validators=[DataRequired()])
    #toLocation = SelectField('To Location', validators=[DataRequired()])
    #quantity = SelectField('Quantity', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Move Product')