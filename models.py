from datetime import date
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship
from app import db, bcrypt, jwt


# Initializes SQLAlchemy object as db variable

# Takes local date into variable
today = date.today()

# Function that entries the 'user'.User object into the db.
def dbCheckUp(user):
    db.create_all()
    user.password = bcrypt.generate_password_hash(user.password, 6).decode("utf8")
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


class User(db.Model):  # User Class table
    __tablename__ = "user"
    __table_args__ = {"schema": "tasklister"}
    # Uses schema 'tasklister'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=True)
    # References relationship  as parent with Task class
    task = relationship("Task")
    token = relationship("Token")

    # Constructor:

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.created_date = today

    # method that calls the function used to entry an user into the db
    def save_user_todb(self):
        dbCheckUp(self)

    # method that verifies if the password is correct or nada
    def verify_password(self):
        user = User.query.filter_by(name=self.name).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password, self.password):
                return True
            else:
                return False

    # method getter that acquires an id from an username : returns user id if it exists, else returns None
    def findId(name):
        user = User.query.filter_by(name=name).first()
        if user is not None:
            return user.id
        else:
            return None


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"schema": "tasklister"}  # Uses schema 'tasklister'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, unique=True)

    def __init__(self, task, user_id):
        self.task = task
        self.user_id = user_id
        self.created_date = today

    def save_task(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_task(uid):
        return Task.query.filter_by(user_id=uid).all()

    def del_task(uid):
        a = Task.query.filter_by(id=uid).first()
        try:
            db.session.delete(a)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()


class Token(db.Model):
    __tablename__ = "Token"
    __table_args__ = {"schema": "tasklister"}

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, unique=True)

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def save_token_todb(self):
        print("self user id is {}".format(self.user_id))
        dbToken = Token.query.filter_by(user_id=self.user_id).first()
        if dbToken is None:
            try:
                db.session.add(self)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()
        elif dbToken is not self.token:
            db.session.delete(dbToken)
            db.session.commit()
            db.session.add(self)
            db.session.commit()
            return self.token
        else:
            return dbToken

