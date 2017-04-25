import os
import jwt
import datetime
from database.user import users, blacklisted_tokens


class AuthManager(object):

    def __init__(self):
        self.handlers = []
        self.secret_key = str(os.urandom(24))

    def get_handlers(self):
        return self.handlers

    def add_handler(self, handler):
        self.handlers.append(handler)

    def add_handler_list(self, handler_list):
        for handler in handler_list:
            self.handlers.append(handler)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                self.secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            print e
            return None

    def decode_auth_token(self, auth_token):
        error = None
        user_id = None

        try:
            payload = jwt.decode(auth_token, self.secret_key)
            if auth_token in blacklisted_tokens:
                error = "Token blacklisted. Please log in again."
            else:
                user_id = str(payload['sub'])
        except jwt.ExpiredSignatureError:
            error = "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            error = "Invalid token. Please log in again."

        return user_id, error

    @classmethod
    def __find_user(cls, user_name):
        for user_id, user in users.items():
            if user["name"] == user_name:
                return user_id, user

        return None, None

    @classmethod
    def check_password(cls, user_name, password):
        user_id, user = cls.__find_user(user_name)
        if user is None:
            return None

        passwd = user["password"]
        if password == passwd:
            return user_id

        return None

    @classmethod
    def check_token(cls, auth_token):
        pass

    @classmethod
    def add_token_to_black_list(cls, auth_token):
        blacklisted_tokens.append(auth_token)
