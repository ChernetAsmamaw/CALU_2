#!/usr/bin/python3
from models.base import BaseModel, Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin

members = Table(
    'members',
    Base.metadata,
    Column('user_id', String(60),
           ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True),
    Column('club_id', String(60),
           ForeignKey('clubs.id', onupdate="CASCADE", ondelete="CASCADE"),
           primary_key=True,)
)

class User(BaseModel, Base, UserMixin):
    """Represents a User"""
    __tablename__ = "users"

    # Requierd attributes for users in order to register as a user
    # to the ketero App.
    username = Column(String(128), nullable=True, unique=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    phone = Column(String(10), nullable=True, unique=True)

    # Optional attributes, users must fillout these infromatin in order
    # to order cards from hospitals.
    place_of_birth = Column(String(128), nullable=True)
    sex = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    country = Column(String(128), nullable=True)
    state = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)

    clubs = relationship('Club', backref='users')

    clubs = relationship("Club",
                            secondary=members,
                            viewonly=False)

    def __init__(self, *args, **kwargs):
        """Initializes User object with super class constructor """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)