from flask_restful import Resource, reqparse
from flask import redirect
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    decode_token,
)
import models


def non_empty_string(s):
    if not s or len(s) < 4:
        raise ValueError("Must not be empty string and have more than 4 characters")
    return s


parser = reqparse.RequestParser()
loginParser = reqparse.RequestParser()
taskParser = reqparse.RequestParser()
delTaskParser = reqparse.RequestParser()

parser.add_argument(
    "name", help="This field cannot be blank", required=True, type=non_empty_string
)
parser.add_argument(
    "password", help="This field cannot be blank", required=True, type=non_empty_string
)
parser.add_argument(
    "email", help="This field cannot be blank", required=True, type=non_empty_string
)


loginParser.add_argument(
    "name", help="This field cannot be blank", required=True, type=non_empty_string
)
loginParser.add_argument(
    "password", help="This field cannot be blank", required=True, type=non_empty_string
)

taskParser.add_argument(
    "task", help="This field cannot be blank", required=True, type=non_empty_string
)

delTaskParser.add_argument("id", help="This field cannot be blank", required=True)


class UserList(Resource):
    def get(self):
        SearchUsers = models.User.query.all()
        UserToDict = {}
        for user in SearchUsers:
            UserToDict[user.id] = user.name
        return UserToDict


class OneUser(Resource):
    def get(self, id):
        try:
            Search = models.User.query.filter_by(id=id).first()
            return f"{Search.id} matches {Search.name}"
        except:
            return f"User with id {id} not found"
            # def post(self) or def get(self) for different http methods.


class SignUp(Resource):
    def post(self):
        req = parser.parse_args()
        print(req)
        new_user = models.User(
            name=req["name"], email=req["email"], password=req["password"]
        )
        try:
            models.User.save_user_todb(new_user)
            return redirect(
                "http://127.0.0.1:5500/task_List/flask-tasklister/login.html", code=302
            )
        except:
            return {"message": "Something went wrong"}, 500


class LogIn(Resource):
    def post(self):
        req = loginParser.parse_args()
        login_creds = models.User(
            name=req["name"], password=req["password"], email=None
        )
        try:
            if models.User.verify_password(login_creds):
                new_token = models.Token(
                    token=create_access_token(
                        identity=models.User.findId(login_creds.name)
                    ),
                    user_id=models.User.findId(login_creds.name),
                )

                return {"token": models.Token.save_token_todb(new_token)}, 200
            elif models.User.verify_password(login_creds) is False:
                return {"message": "Incorrect password"}, 403
            else:
                return {"message": "Incorrect username"}, 403
        except Exception as e:
            return e, 500


class GetTask(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        try:
            a = models.Task.get_task(int(current_user))
            c = []
            for objects in a:
                c.append({"id": objects.id, "task": objects.task})
            return c, 200
        except Exception as e:
            return e, 403


class SaveTask(Resource):
    @jwt_required
    def post(self):
        try:
            try:
                req = taskParser.parse_args()
            except Exception as e:
                return {"error": e}, 403
            current_user = get_jwt_identity()
            task = models.Task(task=req.task, user_id=int(current_user))
            models.Task.save_task(task)
            return {"ok": "ok"}, 200
        except Exception as e:
            return {"error": e}, 403


class DelTask(Resource):
    @jwt_required
    def post(self):
        try:
            req = delTaskParser.parse_args()
            models.Task.del_task(req.id)
            return {}, 200
        except Exception as e:
            print(e)
            return {}, 500
