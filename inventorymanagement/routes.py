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
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT location_name FROM location")
    locations = cursor.fetchall()
    places = []
    for location in locations:
        places.append(location[0])
    
    form = AddProduct()

    if form.validate_on_submit():
        name = form.name.data
        input_values = request.form.getlist('places[]')
        totalquantity = 0
        
        locationinventory = "INSERT INTO `locationinventory`("
        
        for count,place in enumerate(places):
            locationinventory = locationinventory + "`"+ place +"`"
            if count != len(places)-1:
                locationinventory = locationinventory + ","

        locationinventory = locationinventory + ") VALUES ("

        for count,input_value in enumerate(input_values):
            totalquantity = totalquantity + int(input_value)
            locationinventory = locationinventory + "'"+ input_value +"'"
            if count != len(input_values)-1:
                locationinventory = locationinventory + ","
        
        locationinventory = locationinventory + ")"
        location = "INSERT INTO `product`(`product_name`,`product_quantity`,`product_user_id`) VALUES ('"+ name +"','"+ str(totalquantity) +"','"+ str(current_user.user_id) +"')"
        cursor.execute(locationinventory)
        conn.commit()
        cursor.execute(location)
        conn.commit()
        conn.close()
        flash('Done', 'success')
        return redirect(url_for('view_product'))
    return render_template('add_product.html', title='Product', form=form, locations=locations)

@app.route("/edit_product?<int:product_id>", methods=['GET', 'POST'])
def edit_product(product_id):
    form = AddProduct()
    conn = mysql.connect()
    cursor = conn.cursor()
    values = "Select * from product WHERE product_id="+ str(product_id) +""
    values = cursor.execute(values)
    values = cursor.fetchone()
    locations = "SELECT location_name FROM location"
    locations = cursor.execute(locations)
    locations = cursor.fetchall()
    places = []
    for location in locations:
        places.append(location[0])
    inventory = "Select * from locationinventory WHERE locationinventory_id="+ str(product_id) +""
    inventory = cursor.execute(inventory)
    inventory = cursor.fetchone()
    ranges = len(locations)
    quantities = []
    for inventory in inventory:
        quantities.append(inventory)
    quantities.pop(0)
    if form.validate_on_submit():
        name = form.name.data
        input_values = request.form.getlist('places[]')
        print(input_values)
        totalquantity = 0
        locationinventory = "UPDATE `locationinventory` SET "
        
        for index in range(ranges):
            locationinventory = locationinventory + "`" + locations[index][0] + "`='" + str(input_values[index]) +"'"
            totalquantity = totalquantity + int(input_values[index])
            if index != len(input_values)-1:
                locationinventory = locationinventory + ","

        locationinventory = locationinventory + " WHERE `locationinventory_id`=" + str(product_id)
        location = "UPDATE `product` SET `product_name`='"+ name +"',`product_quantity`='"+ str(totalquantity) +"',`product_user_id`='"+ str(current_user.user_id) +"' WHERE product_id="+ str(product_id)
        print(locationinventory)
        cursor.execute(locationinventory)
        conn.commit()
        print(location)
        cursor.execute(location)
        conn.commit()
        conn.close()
        flash('Done', 'success')
        return redirect(url_for('view_product'))
    return render_template('edit_product.html', title='Product', form=form, values=values, locations=locations, quantities=quantities, ranges=ranges)

@app.route("/view_product")
@login_required
def view_product():
    conn = mysql.connect()
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    inventory_places = cursor.execute("SELECT * FROM locationinventory")
    inventory_places = cursor.fetchall()
    return render_template('view_product.html', title='Product', products=products, inventory_places=inventory_places)

########################Locations######################################

@app.route("/add_location", methods=['GET', 'POST'])
@login_required
def add_location():
    form = AddLocation()
    if form.validate_on_submit():
        conn = mysql.connect()
        cursor = conn.cursor()
        count = cursor.execute("SELECT COUNT(*) FROM location WHERE location_name='"+ form.name.data +"'")
        if count == 0:
            cursor.execute("INSERT INTO `location`(`location_name`) VALUES ('"+ (form.name.data).replace(" ", "_") +"')")
            conn.commit()
            cursor.execute("ALTER TABLE locationinventory ADD COLUMN "+ (form.name.data).replace(" ", "_") +" INTEGER DEFAULT 0")
            conn.commit()
            conn.close()
            flash('Location Added', 'success')
            return redirect(url_for('view_location'))
        else:
            conn.close()
            flash('Location Exixts', 'danger')
            return redirect(url_for('add_location'))
        
    return render_template('add_location.html', title='Location', form=form)

@app.route("/edit_location?<int:location_id>", methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    form = AddLocation()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM location WHERE location_id='"+ str(location_id) +"'")
    location = cursor.fetchone()
    if form.validate_on_submit():
        cursor.execute("UPDATE location SET location_name='"+ form.name.data +"' WHERE location_id='"+ str(location_id) +"'")
        conn.commit()
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

@app.route("/add_productmovement?<int:product_id>", methods=['GET', 'POST'])
@login_required
def add_productmovement(product_id):
    form = AddProductMovement()
    print(form)
    conn = mysql.connect()
    cursor = conn.cursor()
    time = datetime.date.today()
    form = AddProductMovement()
    cursor.execute("SELECT product_name FROM product WHERE product_id="+ str(product_id) +"")
    product_name = cursor.fetchone()
    cursor.execute("SELECT location_name FROM location")
    locations = cursor.fetchall()
    ranges = len(locations)
    cursor.execute("SELECT * FROM locationinventory WHERE locationinventory_id="+ str(product_id) +"")
    quantities = cursor.fetchall()
    if form.validate_on_submit():
        product_name = form.name.data
        from_location = form.fromLocation.data
        to_location = form.toLocation.data
        quantity = form.quantity.data
        date = form.timestamp.data
        email = form.email.data
        print(product_name,from_location,to_location,quantity)
        flash('Updated!', 'success')
        return redirect(url_for('view_location'))
    return render_template('add_productmovement.html', title='Movement', form=form, time=time, email=current_user.email, product_name=product_name[0], locations=locations, quantities=quantities, ranges=ranges)

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
