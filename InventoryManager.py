from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '82e65b56c16931a98ff8341e28059a89'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    product = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    product_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    location = db.relationship('Location', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_user_id}', '{self.product_quantity}')"

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20), nullable=False)
    location_product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    location_product_quantity = db.Column(db.Integer, nullable=False)
    location_product_user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Location('{self.location_name}', '{self.location_product_id}', '{self.location_product_quantity}')"

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    from_location = db.Column(db.Integer, nullable=False)
    to_location = db.Column(db.Integer, nullable=False)
    movement_product_quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"ProductMovement('{self.movement_id}', '{self.from_location}', '{self.to_location}', '{self.movement_product_quantity}', '{self.timestamp}')"


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f' Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__=='__main__':
    app.run(debug=True)