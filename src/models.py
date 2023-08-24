from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calu.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = '/img'


db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=True, unique=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(10), nullable=True, unique=True)
    date_of_birth = db.Column(db.String(128), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    nationality = db.Column(db.String(128), nullable=True)
    major = db.Column(db.String(128), nullable=True)
    year_of_study = db.Column(db.String(128), nullable=True)
    study_location = db.Column(db.String(128), nullable=True)
    type = db.Column(db.String(128), nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)

class Club(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String(128), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128), nullable=True, unique=True)
    type = db.Column(db.String(128), nullable=True, unique=True)
    discripton = db.Column(db.String(128), nullable=True)
    member_count = db.Column(db.Integer, nullable=True)
    attraction_count = db.Column(db.Integer, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)

class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.String(128), db.ForeignKey('club.id'), nullable=False)
    user_id = db.Column(db.String(128), db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(128), nullable=True)
    join_date = db.Column(db.String(128), nullable=True)
