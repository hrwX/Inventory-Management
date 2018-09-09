from flask import render_template, url_for, flash, redirect, request
from inventorymanagement import app, db, bcrypt
from inventorymanagement.forms import RegistrationForm, LoginForm, AddProduct, AddLocation, AddProductMovement
from inventorymanagement.models import User, Product, Location, ProductMovement, LocationInventory
from flask_login import login_user, current_user, logout_user, login_required

location = Location.query.all()