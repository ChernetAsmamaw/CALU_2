from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint, get_flashed_messages,g, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, User, Club, Member, Event
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
    clubs = Club.query.filter().all()
    return render_template('clubs-1.html', user=current_user, clubs=clubs)

@app.route('/aboutl')
@login_required
def aboutl():
    return render_template('about-1.html', user=current_user)

# Route for the profile page
@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/terms')
def terms():
    return render_template('terms&conditions.html', user=current_user)



# Route for the demo club page
@app.route('/club_one/<int:club_id>', methods=['GET', 'POST'])
@login_required
def club_one(club_id):
    members = Member.query.filter(Member.club_id == club_id).all()
    member_count = Member.query.filter(Member.club_id == club_id).count()
    club = Club.query.filter(Club.id == club_id).first()
    if club:
        return render_template('club-one.html', user=current_user, club=club,members=members,member_count=member_count)
    else:
        # Handle case when club is not found
        return render_template('home-1.html',user=current_user)
    
@app.route('/join_club/<int:club_id>', methods=['GET', 'POST'])
@login_required
def join_club(club_id):
    if request.method == 'POST':
        club = Club.query.filter(Club.id == club_id).first()
        if club:
            member_count = Member.query.filter(Member.club_id == club.id).count()
            members = Member.query.filter(Member.club_id == club_id).all()
            user=current_user
            user_id=user.id
            print(type(user_id))
            print("yes")
            new_user = Member(
                club_id=club_id,
                user_id=user_id
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Your Have Joined the club!', 'success')
            return render_template('club-one.html', user=current_user, club=club,member_count=member_count,members=members)
        else:
            # Handle case when club is not found
            return render_template('home-1.html',user=current_user)
    club = Club.query.filter(Club.id == club_id).first()
    member_count = Member.query.filter(Member.club_id == club_id).count()
    members = Member.query.filter(Member.club_id == club_id).all()
    return render_template('club-one.html', user=current_user, club=club,member_count=member_count,members=members)

@app.route('/club_one_gallery/<int:club_id>')
@login_required
def club_one_gallery(club_id):
    club = Club.query.filter(Club.id == club_id).first()
    return render_template('club-one-gallery.html', user=current_user, club=club)


@app.route('/club_one_events/<int:club_id>')
@login_required
def club_one_events(club_id):
    club = Club.query.filter(Club.id == club_id).first()
    return render_template('club-one-event.html', user=current_user, club=club)

@app.route('/club_one_about/<int:club_id>')
@login_required
def club_one_about(club_id):
    club = Club.query.filter(Club.id == club_id).first()
    return render_template('club-one-about.html', user=current_user, club=club)


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

        is_first_user = User.query.first() is None
        if is_first_user:
            type = 'admin'
        else:
            type = 'user'

        # Create a new user object
        new_user = User(
            email=email,
            password=hashed_password,
            type=type    
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
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        gender = request.form['gender']
        nationality = request.form['nationality']
        major = request.form['major']
        year_of_study = request.form['year_of_study']
        study_location = request.form['study_location']
        file = request.files['image']
        
        # Process the uploaded file here
        user = User.query.filter_by(email=user1.email).first()
        try:
            # Assuming 'file' is the uploaded file object and 'user' is the user object

            # Save the file
            file.save('/static/uploads/' + file.filename)

            # Secure the filename
            filename = secure_filename(file.filename)

            # Assign the encoded filename to the user's image attribute
            user.image = filename.encode('utf-8')

            # Printing the result
            print("File saved and user image updated successfully.")
        
        
        #print("An error occurred:", str(e))
        except Exception as e:
            pass
        
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
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


# Route for the admin's club creation page
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
        try:
            file.save('static/uploads/' + file.filename)

        except Exception as e:
            pass
        filename = secure_filename(file.filename)
        # Create a new user object
        new_club = Club(
            name=name,
            discripton=discripton,
            type=type,
            owner_id=user.id,
            image=filename.encode('utf-8')
        )

        # Add the new user to the database
        db.session.add(new_club)
        db.session.commit()

        flash('You have created the club', 'success')
        return redirect(url_for('create'))
    clubs = Club.query.filter().all()
    return render_template('/admin/create.html', user=current_user,clubs=clubs)


# Route for the admin's event creation page
@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        admission = request.form['admission']
        location = request.form['location']
        rsvp = request.form['rsvp']
        link = request.form['link']

        event = Event.query.filter_by(name=name).first()
        if event:
            flash('Event already exist', 'error')
            return redirect(url_for('event'))

        # Hash the password
        user = current_user

        # Save the uploaded image if present
        file = request.files['image']

        # Process the uploaded file here
        try:
            file.save('static/uploads/' + file.filename)

        except Exception as e:
            pass

        filename = secure_filename(file.filename)

        # Create a new user object
        new_event = Event(
            name=name,
            description=description,
            date=date,
            time=time,
            admission=admission,
            location=location,
            rsvp=rsvp,
            link=link,
            image=filename.encode('utf-8')
        )

        # Add the new user to the database
        db.session.add(new_event)
        db.session.commit()

        flash('You have created an event', 'success')
        return redirect(url_for('event'))
    
    event = Event.query.filter().all()

    return render_template('/admin/event.html', user=current_user, event=event)


@app.route('/events_admin')
@login_required
def events_admin():
    event = Event.query.filter().all()
    return render_template('/admin/events_admin.html', user=current_user, event=event)


@app.route('/requests')
@login_required
def requests():
    return render_template('/admin/requests.html', user=current_user)

@app.route('/clubs_admin')
@login_required
def clubs_admin():
    clubs = Club.query.filter().all()
    return render_template('/admin/clubs_admin.html', user=current_user,clubs=clubs)

@app.route('/create_club', methods=['GET', 'POST'])
@login_required
def create_club():
    # Render the signup page
    return render_template('reg.html')


# Route for the admin's profile page
@app.route('/admin_profile')
def admin_profile():
    return render_template('/admin/admin_profile.html', user=current_user)


@app.route('/edit_admin_profile', methods=['GET', 'POST'])
@login_required
def edit_admin_profile():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    if request.method == 'POST':
        user1 = current_user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        #reverse the hashed password
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        gender = request.form['gender']
        nationality = request.form['nationality']
        major = request.form['major']
        year_of_study = request.form['year_of_study']
        study_location = request.form['study_location']
        file = request.files['image']
    # Process the uploaded file here
        user = User.query.filter_by(email=user1.email).first()
        try:
            # Assuming 'file' is the uploaded file object and 'user' is the user object

            # Save the file
            file.save('static/uploads/' + file.filename)

            # Secure the filename
            filename = secure_filename(file.filename)

            # Assign the encoded filename to the user's image attribute
            user.image = filename.encode('utf-8')

            # Printing the result
            print("File saved and user image updated successfully.")

        except Exception as e:
            #print("An error occurred:", str(e))
            pass
        
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.username=username
        user.date_of_birth=date_of_birth
        user.phone=phone
        user.gender=gender
        user.nationality=nationality
        user.major=major
        user.year_of_study=year_of_study
        user.study_location=study_location
        
        

        db.session.commit()
        return redirect(url_for('admin_profile'))
    return render_template('/admin/admin_profile.html',user=current_user)




# run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)