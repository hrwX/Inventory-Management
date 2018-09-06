from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '82e65b56c16931a98ff8341e28059a89'

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