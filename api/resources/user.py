import logging
from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc


@doc(description='Api for notes.', tags=['Users'])
class UserResource(MethodResource):
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        # language=YAML
        """
        Get User by id
        ---
        tags:
            - Users
        parameters:
             - in: path
               name: user_id
               type: integer
               required: true
               default: 1
        responses:
           200:
               description: A single user item
               schema:
                   id: User
                   properties:
                       id:
                           type: integer
                           description: user id
                           default: 1
                       username:
                           type: string
                           description: The name of the user
                           default: Steven Wilson
                       is_staff:
                           type: boolean
                           description: user is staff
                           default: false
                       role:
                           type: string
                           description: ...
                           default: simple_user
        """
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, error=f"User with id={user_id} not found")
        # return user_schema.dump(user), 200
        return user, 200

    @use_kwargs(UserRequestSchema, location=('json'))
    @marshal_with(UserSchema, code=201)
    # @auth.login_required(role="admin")
    def put(self, user_id, **kwargs):
        # language=YAML
        """
        Edit User by id
        ---
        tags:
            - Users
        """
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        user_data = UserModel(**kwargs)
        user = UserModel.query.get(user_id)
        user.username = user_data["username"]
        user.save()
        return user, 200

    @auth.login_required
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!


@doc(description='Api for notes.', tags=['Users'])
class UsersListResource(MethodResource):
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    @use_kwargs(UserRequestSchema, location=('json'))
    @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # parser.add_argument("password", required=True)
        user = UserModel(**kwargs)
        # user = UserModel(**user_data)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        logging.info("User create successfully")
        # return user_schema.dump(user), 201
        return user, 201

@doc(description='Api for notes.', tags=['Users'])
class UsersSeacrhResource(MethodResource):
    @marshal_with(UserSchema)
    def get(self, namepart):
        users = UserModel.query.filter(UserModel.username.like(f"%{namepart}%")).all()
        return users, 201