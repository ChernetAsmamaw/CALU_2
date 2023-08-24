from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint, get_flashed_messages,g, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, User, Club, Member
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from datetime import date, datetime, timedelta
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from sqlalchemy import and_


app = app

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load the user from the database
@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    user = None
    if not user:
        user = User.query.get(int(user_id))
    return user

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
@login_required
def homel():
    return render_template('home-1.html', user=current_user)

@app.route('/clubsl')
@login_required
def clubsl():
    return render_template('clubs-1.html', user=current_user)

@app.route('/aboutl')
@login_required
def aboutl():
    return render_template('about-1.html', user=current_user)

# Route for the profile page
@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


# Route for the demo club page
@app.route('/club_one')
def club_one():
    return render_template('club-one.html', user=current_user)

@app.route('/club_one_gallery')
def club_one_gallery():
    return render_template('club-one-gallery.html', user=current_user)

@app.route('/club_one_events')
def club_one_events():
    return render_template('club-one-events.html', user=current_user)

@app.route('/club_one_about')
def club_one_about():
    return render_template('club-one-about.html', user=current_user)



# Route for handling the registration page logic
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']


        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            return redirect(url_for('login'))
        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(
            email=email,
            password=hashed_password,
            type='admin'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully! Please log in.', 'success')
        return redirect(url_for('signup'))

    return render_template('signup.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user is a user
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Log in the user
            if user.type == 'admin':
                flash('You have logged in successfully!', 'success')
                login_user(user, remember=True)
                return redirect(url_for('admin'))
            flash('You have logged in successfully!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('homel'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')


# Route for handling the logout page logic
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))


# Route for handling the profile page logic
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    if request.method == 'POST':
        user1 = current_user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        #reverse the hashed password
        password = request.form['password']
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        gender = request.form['gender']
        nationality = request.form['nationality']
        major = request.form['major']
        year_of_study = request.form['year_of_study']
        study_location = request.form['study_location']

        user = User.query.filter_by(email=user1.email).first()
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.password=password
        user.username=username
        user.date_of_birth=date_of_birth
        user.phone=phone
        user.gender=gender
        user.nationality=nationality
        user.major=major
        user.year_of_study=year_of_study
        user.study_location=study_location
        

        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html',user=current_user)








@app.route('/admin')
@login_required
def admin():
    return render_template('/admin/admin.html', user=current_user)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        discripton = request.form['discripton']
        type = request.form['type']
        club = Club.query.filter_by(name=name).first()
        if club:
            flash('club already exist', 'error')
            return redirect(url_for('create'))

        # Hash the password
        user = current_user
        # Save the uploaded image if present
        file = request.files['image']
    # Process the uploaded file here
        file.save('static/uploads/' + file.filename)
    #filename = secure_filename(f.filename)
        # Create a new user object
        new_club = Club(
            name=name,
            discripton=discripton,
            type=type,
            owner_id=user.id,
            #image=filename.encode('utf-8')
        )

        # Add the new user to the database
        db.session.add(new_club)
        db.session.commit()

        flash('You have created the club', 'success')
        return redirect(url_for('create'))
    return render_template('/admin/create.html', user=current_user)

@app.route('/requests')
@login_required
def requests():
    return render_template('/admin/requests.html', user=current_user)

@app.route('/clubs_admin')
@login_required
def clubs_admin():
    return render_template('/admin/clubs_admin.html', user=current_user)

@app.route('/create_club', methods=['GET', 'POST'])
@login_required
def create_club():
    

    # Render the signup page
    return render_template('reg.html')








# run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
    app.run(debug=True)