from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from inventorymanagement.models import User

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

class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    location = IntegerField('Product Location', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class AddLocation(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')

class AddProductMovement(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    product_id = IntegerField(validators=[DataRequired()])
    fromLocation = StringField('From Location', validators=[DataRequired()])
    fromLocationId = IntegerField(validators=[DataRequired()])
    toLocation = StringField('To Location', validators=[DataRequired()])
    toLocationId = IntegerField(validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    timestamp = DateTimeField(validators=[DataRequired()])
    submit = SubmitField('Move Product')
