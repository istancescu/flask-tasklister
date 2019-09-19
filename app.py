from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import models
import routes


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(routes.SignUp, '/signup')
api.add_resource(routes.LogIn, '/login')
api.add_resource(routes.UserList, '/users')
api.add_resource(routes.OneUser, '/user/<int:id>/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

# TODO:
# --> ADD BCrypt                    <----> done <---->
# --> ADD Register Handle (request) <----> done <---->
# --> ADD Login Handle (request)    <----> done  <---->
# --> ADD JWT                       <----> TBA   <---->
# --> ACP IDEA?                    <----> idea <---->
