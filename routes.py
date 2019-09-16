from flask_restful import Resource

from models import User


class UserList(Resource):
    def get(self):
        SearchUsers = User.query.all()
        UserToDict = {}
        for user in SearchUsers:
            UserToDict[user.id] = user.name
        return (UserToDict)


class OneUser(Resource):
    def get(self, id):
        try:
            Search = User.query.filter_by(id=id).first()
            return (f"{Search.id} matches {Search.name}")
        except:
            return (f"User with id {id} not found")
            # def post(self) or def get(self) for different http methods.
