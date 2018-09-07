from flask import render_template, url_for, flash, redirect
from inventorymanagement import app, db, bcrypt
from inventorymanagement.forms import RegistrationForm, LoginForm
from inventorymanagement.models import User, Product, Location, ProductMovement
from flask_login import login_user, current_user, logout_user, login_required

posts=[
    {
        'author': 'Abc',
        'title': 'Post 1',
        'content': 'First post content',
        'data_posted': 'april20, 2018'
    },
    {
        'author': 'Abc',
        'title': 'Post 2',
        'content': 'First post content',
        'data_posted': 'april20, 2018'
    }, 
    {
        'author': 'Abc',
        'title': 'Post 3',
        'content': 'First post content',
        'data_posted': 'april20, 2018'
    }, 
    {
        'author': 'Abc',
        'title': 'Post 4',
        'content': 'First post content',
        'data_posted': 'april20, 2018'
    }  
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user.user_id, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)