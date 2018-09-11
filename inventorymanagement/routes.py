import datetime
from flask import render_template, url_for, flash, redirect, request
from inventorymanagement import app, bcrypt, mysql, db
from inventorymanagement.forms import RegistrationForm, LoginForm, AddProduct, AddLocation, AddProductMovement
from inventorymanagement.models import User
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, SelectField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

@app.route("/")
@app.route("/anon")
def anon():
    return redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title="About")

########################Users######################################

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
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('anon'))

########################Products######################################

@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    #queries = Location.query.all()
    locations = []
    
    for query in queries:
        locations.append(str(query).replace("'", "")) #mumbai_location
    
    form = AddProduct()

    input_values = request.form.getlist('places[]')
    #for input_value in input_values:
    #    print(input_value)
    
    location_values = dict(zip(locations, input_values))
    print(location_values)
    
    string = "product_name=form.name.data,"
    for query in queries:
        string_join = ""+ (str(query) + "_location").replace("'", "") +"=form."+ (str(query) + "_location").replace("'", "") +".data,"
        string = string + string_join
    string_join = "product_user_id=current_user"
    string = string + string_join

    if form.validate_on_submit():
        for location in locations:
            print(form.name.data)
   
    #product = Product(string)
    return render_template('add_product.html', title='Product', form=form, locations=locations)

@app.route("/edit_product")
@login_required
def edit_product():
    form = AddProduct()
    return render_template('edit_product.html', title='Product', form=form)

@app.route("/view_product")
@login_required
def view_product():
    return render_template('view_product.html', title='Product')

########################Locations######################################

@app.route("/add_location", methods=['GET', 'POST'])
@login_required
def add_location():
    form = AddLocation()
    if form.validate_on_submit():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `location`(`location_name`) VALUES ('"+ form.name.data +"')")
        conn.commit()
        location = (form.name.data).replace(" ","")
        print(location)
        print("ALTER TABLE locationinventory ADD COLUMN "+ form.name.data +" INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE locationinventory ADD COLUMN "+ (form.name.data).replace(" ", "_") +" INTEGER DEFAULT 0")
        conn.commit()
        conn.close()
        print("INSERT INTO `location`(`location_name`) VALUES ('"+ form.name.data +"')")
        print("ALTER TABLE locationinventory ADD COLUMN "+ form.name.data +" INTEGER DEFAULT 0")
        flash('Location Added')
        return redirect(url_for('view_location'))
    return render_template('add_location.html', title='Location', form=form)

@app.route("/edit_location?<int:location_id>", methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    form = AddLocation()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM location WHERE location_id='"+ str(location_id) +"'")
    conn.commit()
    location = cursor.fetchone()
    if form.validate_on_submit():
        cursor.execute("UPDATE location SET location_name='"+ form.name.data +"' WHERE location_id='"+ str(location_id) +"'")
        print(cursor)
        flash('Updated!', 'success')
        return redirect(url_for('view_location'))
    elif request.method == 'GET':
        form.name.data = location_id
    return render_template('edit_location.html', title='Location', form=form, location=location)

@app.route("/view_location")
@login_required
def view_location():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM location")
    locations = cursor.fetchall()
    return render_template('view_location.html', title='Location', locations=locations) 

########################ProductMovements######################################

@app.route("/add_productmovement", methods=['GET', 'POST'])
@login_required
def add_productmovement():
    time = datetime.date.today()
    form = AddProductMovement()
    return render_template('add_productmovement.html', title='Movement', form=form, time=time)

@app.route("/edit_productmovement")
@login_required
def edit_productmovement():
    form = AddProductMovement()
    return render_template('edit_productmovement.html', title='Movement', form=form)

@app.route("/view_productmovement")
@login_required
def view_productmovement():
    return render_template('view_productmovement.html', title='Movement')

########################Sales######################################

@app.route("/view_sales")
@login_required
def view_sales():
    return render_template('view_sales.html', title='Sales')

@app.route("/bcrypt")
def bcrypter():
    hashed_password = bcrypt.generate_password_hash('123456').decode('utf-8')
    return render_template('bcrypt.html', title='Movement', hashed_password=hashed_password)