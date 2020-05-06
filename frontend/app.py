from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import models
import routes
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@127.0.0.1:3306/"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "uihgsdruih1278SJB12#@!"

api.add_resource(routes.SignUp, "/signup")
api.add_resource(routes.LogIn, "/login")
api.add_resource(routes.UserList, "/users")
api.add_resource(routes.GetTask, "/self/user/get_task")
api.add_resource(routes.SaveTask, "/self/user/save_task")
api.add_resource(routes.DelTask, "/self/user/del_task")
api.add_resource(routes.OneUser, "/user/<int:id>/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

# TODO:
# --> ADD BCrypt                    <----> done <---->
# --> ADD Register Handle (request) <----> done <---->
# --> ADD Login Handle (request)    <----> done <---->
# --> ADD JWT                       <----> done <---->
# --> ADD JWT: frontend             <----> done <---->
# --> ADD Task: self                <----> done <---->
# --> ADD Task: get                 <----> done <---->
# --> ADD Task: set                 <----> done <---->
# --> MINOR REFACTORING             <----> done <---->
# --> ACP IDEA?                     <----> idea <---->
