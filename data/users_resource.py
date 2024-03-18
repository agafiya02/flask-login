from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from data import session
from data.users import User


def abort_if_users_not_found(users_id):
    session1 = session.create_session()
    users = session1.query(User).get(users_id)
    if not users:
        abort(404, message=f"users {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session1 = session.create_session()
        users = session1.query(User).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session1 = session.create_session()
        users = session1.query(User).get(users_id)
        session1.delete(users)
        session1.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('modified_date', required=True)


class UsersListResource(Resource):
    def get(self):
        session1 = session.create_session()
        users = session1.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session1 = session.create_session()
        users = User(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session1.add(users)
        session1.commit()
        return jsonify({'id': users.id})
