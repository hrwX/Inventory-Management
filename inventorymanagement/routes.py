import datetime
from flask import render_template, url_for, flash, redirect, request
from inventorymanagement import app, bcrypt, mysql, db
from inventorymanagement.forms import RegistrationForm, LoginForm, AddProduct, AddLocation, ProductMovement
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
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(product_id) FROM product WHERE user_id="+ str(current_user.user_id) +"")
    products = cursor.fetchone()
    cursor.execute("SELECT COUNT(location_id) FROM location")
    locations = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM productmovement WHERE user_id="+ str(current_user.user_id) +"")
    movements = cursor.fetchone()
    sales = 5
    return render_template('home.html', title='Home', products=products[0], locations=locations[0], sales=sales, movements=movements[0])

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

        locationinventory = locationinventory + ",`user_id`) VALUES ("

        for count,input_value in enumerate(input_values):
            totalquantity = totalquantity + int(input_value)
            locationinventory = locationinventory + "'"+ input_value +"'"
            if count != len(input_values)-1:
                locationinventory = locationinventory + ","
        
        locationinventory = locationinventory + ",'"+ str(current_user.user_id) +"')"
        location = "INSERT INTO `product`(`product_name`,`product_quantity`,`user_id`) VALUES ('"+ name +"','"+ str(totalquantity) +"','"+ str(current_user.user_id) +"')"
        print(locationinventory)
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
    print(quantities)
    for count in range(2):
        quantities.pop(0)
    print(quantities)
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
        location = "UPDATE `product` SET `product_name`='"+ name +"',`product_quantity`='"+ str(totalquantity) +"' WHERE product_id="+ str(product_id)
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

@app.route("/product_info?<int:product_id>", methods=['GET', 'POST'])
def product_info(product_id):
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
    for count in range(2):
        quantities.pop(0)
    return render_template('product_info.html', title='Product', form=form, values=values, locations=locations, quantities=quantities, ranges=ranges)


@app.route("/view_product")
@login_required
def view_product():
    conn = mysql.connect()
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM product WHERE user_id='"+ str(current_user.user_id)+"'")
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
        count = cursor.execute("SELECT location_name FROM location WHERE location_name='"+ (form.name.data).replace(" ", "_") +"'")
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
    form = ProductMovement()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name FROM product WHERE product_id="+ str(product_id) +"")
    product_name = cursor.fetchone()
    cursor.execute("SELECT location_name FROM location")
    locations = cursor.fetchall()
    time = datetime.date.today()
    ranges = len(locations)
    cursor.execute("SELECT * FROM locationinventory WHERE locationinventory_id="+ str(product_id) +"")
    inventory = cursor.fetchone()
    quantities = []
    for inventory in inventory:
        quantities.append(inventory)
    for count in range(2):
        quantities.pop(0)
    print(quantities[5])
    if form.validate_on_submit():
        product_name = form.name.data
        from_location = request.values.get('fromLocation')
        to_location = request.values.get('toLocation')
        quantity = request.values.get('quantity')
        date = request.values.get('timestamp')
        email = request.values.get('email')
        query = "SELECT "+ str(from_location) +","+ str(to_location) +" FROM locationinventory WHERE locationinventory_id="+ str(product_id) +""
        cursor.execute(query)
        value = cursor.fetchone()
        from_location_qty = value[0] - int(quantity)
        to_location_qty = value[1] + int(quantity)
        query = "UPDATE locationinventory SET "+ str(from_location) +"='"+ str(from_location_qty) +"', "+ str(to_location) +"='"+ str(to_location_qty) +"' WHERE locationinventory_id="+ str(product_id) +""
        print(query)
        cursor.execute(query)
        conn.commit()
        query = "INSERT INTO `productmovement`(`product_id`, `product_name`, `from_location_name`, `to_location_name`, `product_quantity`, `timestamp`, `user_id`) VALUES ('"+ str(product_id) +"','"+ form.name.data +"','"+ str(from_location) +"','"+ str(to_location) +"','"+ quantity +"','"+ date +"','"+ str(current_user.user_id) +"')"
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        flash('Updated!', 'success')
        return redirect(url_for('view_location'))
    return render_template('add_productmovement.html', title='Movement', form=form, time=time, email=current_user.email, product_name=product_name[0], locations=locations, quantities=quantities, ranges=ranges)

@app.route("/edit_productmovement?<int:productmovement_id>")
@login_required
def edit_productmovement(productmovement_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productmovement WHERE productmovement_id="+ str(productmovement_id) +"")
    query = cursor.fetchone()
    product_id = query[1]
    from_location = query[3]
    to_location = query[4]
    quantity = query[5]
    cursor.execute("SELECT "+ str(from_location) +","+ str(to_location) +" FROM locationinventory WHERE locationinventory_id="+ str(product_id) +"")
    inventory = cursor.fetchone()
    from_location_qty = inventory[0] + quantity
    to_location_qty = inventory[1] - quantity
    cursor.execute("UPDATE locationinventory SET "+ str(from_location) +"='"+ str(from_location_qty) +"', "+ str(to_location) +"='"+ str(to_location_qty) +"' WHERE locationinventory_id="+ str(product_id) +"")
    conn.commit()
    cursor.execute("DELETE FROM productmovement WHERE productmovement_id="+ str(productmovement_id) +"")
    conn.commit()
    return redirect(url_for('view_productmovement'))
    return render_template('', title='Movement', form=form)

@app.route("/view_productmovement")
@login_required
def view_productmovement():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productmovement WHERE user_id="+ str(current_user.user_id) +"")
    movements = cursor.fetchall()
    counts = len(movements)
    return render_template('view_productmovement.html', title='Movement', movements=movements, counts=counts)