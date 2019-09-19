from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from app import db, bcrypt


# Initializes SQLAlchemy object as db variable

# Takes local date into variable
today = date.today()


def dbCheckUp(obj1):
    db.create_all()
    obj1.password = bcrypt.generate_password_hash(
        obj1.password, 6).decode('utf8')
    try:
        db.session.add(obj1)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


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

    def save_user_todb(self):
        dbCheckUp(self)

    def verify_password(self):
        user = User.query.filter_by(name=self.name).first()
        if user is not None:
            if (bcrypt.check_password_hash(user.password, self.password)):
                return True
            else:
                return False
            return ValueError


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {'schema': 'tasklister'}  # Uses schema 'tasklister'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, id, task, user_id):
        self.id = id
        self.task = task
        self.user_id = user_id
        self.created_date = today

    def save_task_todb(self):
        dbCheckUp(self)
