from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

# Initializes SQLAlchemy object as db variable
db = SQLAlchemy()

# Takes local date into variable
today = date.today()


class User(db.Model):  # User Class table
    __tablename__ = "user"
    __table_args__ = {'schema': 'tasklister'}  # Uses schema 'tasklister'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=True)
    # References relationship  as parent with Task class
    task = relationship("Task")

    # Constructor:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.created_date = today


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {'schema': 'tasklister'}  # Uses schema 'tasklister'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
