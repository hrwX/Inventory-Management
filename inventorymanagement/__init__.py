from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = '82e65b56c16931a98ff8341e28059a89'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#db = SQLAlchemy(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'inventory_management'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from inventorymanagement import routes #to avoid circular imports issue