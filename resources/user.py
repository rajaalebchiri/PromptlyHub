"""Authentication Routes"""
from flask.views import MethodView
from flask import current_app
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

from db import db
from blocklist import BLOCKLIST

from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from tasks import send_user_registration_email

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegistration(MethodView):
    """User Registration Route"""

    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        """Create a new user registration"""
        if UserModel.query.filter(
            (UserModel.username == user_data["username"]) |
            (UserModel.email == user_data["email"])
        ).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        db.session.add(user)
        db.session.commit()

        # if you want to use background worker to send emails
        # current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        send_user_registration_email(user.email, user.username)

        return {"message": "User created successfully."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """User Operations"""

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user information"""
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        """Delete a user"""
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User Deleted."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    """User Login Operation"""

    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Login"""

        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"access_token": access_token,
                    "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials")


@blp.route("/logout")
class UserLogout(MethodView):
    """User Logout Operation"""

    @jwt_required()
    def post(self):
        """logout using BLOCKLIST"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    """refresh token"""

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
