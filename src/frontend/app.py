from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from uuid import uuid4
from models import storage
from models.user import User
from hashlib import md5
from flask_login import login_user, login_required, logout_user, current_user

# Import the LoginManager and configure it on the app level.
from flask_login import LoginManager


app = Flask(__name__)
# You must config the secret key at the app level before specifying any routes.
app.config['SECRET_KEY'] = 'here is the secret for our application'


# You must close the db connection
@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


# Initialize the app with the LoginMananger
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)


# Load the user data
@login_manager.user_loader
def load_user(id):
    return storage.get(User, id)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/clubs')
def clubs():
    return render_template('clubs.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/homel')
def homel():
    return render_template('home-1.html')


@app.route('/clubsl')
def clubsl():
    return render_template('clubs-1.html')


@app.route('/aboutl')
def aboutl():
    return render_template('about-1.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/logout', strict_slashes=False)
@login_required
def logut():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        # Get the form data
        users = storage.all(User).values()
        emails = [user.email for user in users]
        data = request.form
        print(data)

        # Only access the data that is sent by the html form.
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('password')

        # Remove unnecessary checks for first name, last name and etc ..
        if email in emails:
            flash("Email address already exists", category='error')
        elif len(password) < 6 or len(password) > 15:
            flash("Password must be 6 - 15 characters length",
                  category='error')
        elif password != confirm_password:
            flash("Passwords don't match", category='error')
        else:
            # Only send email and password to the database as other fields are not provided from the frontend side.
            info = {
                "email": email, "password": password
            }
            new_account = User(**info)
            new_account.save()
            print(new_account)
            login_user(new_account, remember=True)
            flash("Account created successfully", category='success')
            return redirect(url_for('home1'))

    return render_template("signup.html", user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
