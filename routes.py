from flask_restful import Resource, reqparse
from flask import request, redirect

import models


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


parser = reqparse.RequestParser()
parser.add_argument(
    'name', help='This field cannot be blank', required=True,  type=non_empty_string)
parser.add_argument(
    'password', help='This field cannot be blank', required=True, type=non_empty_string)
parser.add_argument(
    'email', help='This field cannot be blank', required=True, type=non_empty_string)


class UserList(Resource):
    def get(self):
        SearchUsers = models.User.query.all()
        UserToDict = {}
        for user in SearchUsers:
            UserToDict[user.id] = user.name
        return (UserToDict)


class OneUser(Resource):
    def get(self, id):
        try:
            Search = models.User.query.filter_by(id=id).first()
            return (f"{Search.id} matches {Search.name}")
        except:
            return (f"User with id {id} not found")
            # def post(self) or def get(self) for different http methods.


class SignUp(Resource):
    def post(self):

        req = parser.parse_args()
        new_user = models.User(
            name=req['name'],
            email=req['email'],
            password=req['password']
        )
        try:
            models.User.save_user_todb(new_user)
            return redirect("http://127.0.0.1:5500", code=302)
        except:
            return {'message': 'Something went wrong'}, 500
