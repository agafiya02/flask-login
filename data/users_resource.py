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
        user = session1.query(User).get(users_id)
        return jsonify({
            'users': user.to_dict(only=())
        })

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
parser.add_argument('is_private', required=True)
parser.add_argument('address', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('modified_date', required=True)


class UsersListResource(Resource):
    def get(self):
        session1 = session.create_session()
        users = session1.query(User).all()
        return jsonify(
            {'users':
                [item.to_dict(only=()) for item in users]}
        )

    def post(self):
        args = parser.parse_args()
        session1 = session.create_session()
        users = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            is_private=args['is_private'],
            address=args['address'],
            about=args['about'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            modified_date=args['modified_date']
        )
        session1.add(users)
        session1.commit()
        return jsonify({'id': users.id})
