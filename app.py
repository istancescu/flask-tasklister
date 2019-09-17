from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import models
import routes


app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(routes.SignUp, '/signup')
api.add_resource(routes.UserList, '/users')
api.add_resource(routes.OneUser, '/user/<int:id>/')

#        - metarolling for db.add() -
#     try:
#         db.session.add(u)
#         db.session.commit()
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

# TODO:
# --> ADD BCrypt( from passlib.hash import bcrypt )
# --> ADD Register Handle (request)
# --> ADD Login Handle (request)
# --> ACP IDEEA?
