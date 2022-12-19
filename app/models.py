from app import db
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin

Base = declarative_base()

class User(db.Model, UserMixin, Base):
    # __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    meals = db.relationship('Meal', secondary='user_meals', backref='users')

class Meal(db.Model, Base):
    # __tablename__ = "meal_table"
    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.String(30), nullable=False)
    snack = db.Column(db.String(30), nullable=False)
    drink = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100))
    likes = db.Column(db.Integer)

user_meals = db.Table('user_meals',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id')),
)