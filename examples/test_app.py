from flask import Flask, jsonify
from flask import abort, make_response
from flask import request
from flask import url_for

from flask_httpauth import HTTPBasicAuth

import os
import time
from md5 import md5

from OpenSSL import SSL

# for tokens
import jwt
import datetime
import copy
import uuid
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

users = {
    "a3235dec-58a8-4716-90f5-6df2423ffb54": {
        "name": "andrew",
        "password": "123",
        "email": "email@gmail.com",
        "md5_hash": "202cb962ac59075b964b07152d234b70"
    },

    "f965d4cf-1256-4b3d-93dd-e3f7ecfa08f9": {
        "name": "test",
        "password": "1234",
        "email": "email@gmail.com",
        "md5_hash": "81dc9bdb52d04dc20036dbd8313ed055"
    },

    "a2598c98-1f62-4a6b-815d-03497522a7a3": {
        "name": "admin",
        "password": "admin",
        "email": "email@gmail.com",
        "md5_hash": ""
    },

    "c1002399-a3b0-4fe8-8b68-597977c03e97": {
        "name": "user",
        "password": "user",
        "email": "email@gmail.com",
        "md5_hash": ""
    }
}

# if users exit then append this token in this list
blacklisted_tokens = []

# create SECRET_KEY -> os.urandom(24)
SECRET_KEY = "\xa9\xc8'\xac\x99\xdd\x04\x9fh\xd0*\xa8Q\xf8\xa0FZ6d\xf6\xed\x83&\xac"


def find_user(username):
    for user_id, user in users.items():
        if username == user["name"]:
            return user_id, copy.deepcopy(user)
    return None, None


def find_user_by_id(user_id):
    try:
        user = users[user_id]
    except Exception:
        return None
    return user


@auth.get_password
def get_pw(username):
    user_id, user = find_user(username)
    if user is not None:
        if user["md5_hash"] == "":
            return user["password"]
        else:
            return user["md5_hash"]
    return None


@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': map(make_public_task, tasks)})


@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    print "receive request"
    time.sleep(5)
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # time.sleep(5)
    if not request.json or not 'title' in request.json:
        abort(400)

    print "request-> ", request
    print "request.json-> ", request.json

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done': False,
    }
    
    tasks.append(task)
    return jsonify({'task':task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


# @app.route('/')
# def index():
#     response = make_response(jsonify({'tasks': tasks}), 201)
#     response.set_cookie("username", "the username")
#     return response

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return None


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        if auth_token in blacklisted_tokens:
            return 0#"Token blacklisted. Please log in again."
        else:
            return str(payload['sub'])
    except jwt.ExpiredSignatureError:
        return 1#"Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return 2#"Invalid token. Please log in again."


@app.route('/auth/register', methods=['POST'])
def register_api():
    request_dict = request.json
    name = request_dict["name"]
    password = request_dict["password"]
    user_id, user = find_user(name)
    print request_dict
    print user
    # return make_response(jsonify({"status": "OK"})), 201

    if user is None:
        # add user
        user = {
            "name": str(name),
            "password": str(password),
            "md5_hash": ""
        }
        user_id = str(uuid.uuid4())
        users.update({user_id: user})
        print users
        auth_token = encode_auth_token(user_id)
        print auth_token
        response_object = {
            "status": "success",
            "message": "Successfully registered",
            "auth_token": auth_token.decode()
        }
        print response_object
        return make_response(jsonify(response_object)), 201
    else:
        response_object = {
            "status": "fail",
            "message": "User already exist. Please Log in",
        }
        return make_response(jsonify(response_object)), 202


def check_password(user, password):
    result = True
    passwd = user["password"]
    if password != passwd:
        result = False

    return result


@app.route('/auth/login', methods=['POST'])
def login_api():
    request_dict = request.json
    try:
        name = request_dict["name"]
        password = request_dict["password"]
        user_id, user = find_user(name)
        if user and check_password(user, password):
            auth_token = encode_auth_token(user_id)
            if auth_token is not None:
                response_object = {
                    "status":  "success",
                    "message": "Successfully logged in",
                    "auth_token": auth_token.decode()
                }
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                "status": "fail",
                "message": "User does not exist"
            }
            return make_response(jsonify(response_object)), 404

    except Exception as e:
        print e
        response_object = {
            "status": "fail",
            "message": "Try again"
        }
        return make_response(jsonify(response_object)), 500


@app.route('/auth/logout', methods=['POST'])
def logout_api():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        user_id = decode_auth_token(auth_token)
        print user_id
        if isinstance(user_id, str):
            blacklisted_tokens.append(auth_token)
            response_object = {
                "status": "success",
                "message": "Successfully logged out"
            }
            return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                "status": "fail",
                "message": user_id
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token"
        }
        return make_response(jsonify(response_object)), 403


@app.route('/auth/status', methods=['GET'])
def user_api():
    auth_header = request.headers.get("Authorization")
    print auth_header
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    print auth_token
    if auth_token:
        user_id = decode_auth_token(auth_token)
        print user_id
        if isinstance(user_id, str):
            user = find_user_by_id(user_id)
            if user is not None:
                response_object = {
                    "status": "success",
                    "data": {
                        "email": str(user["email"]),
                        "name": str(user["name"])
                    }
                }
                return make_response(jsonify(response_object)), 200

            response_object = {
                "status": "fail",
                "message": "User was not found"
            }
            return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                "status": "fail",
                "message": user_id
            }
        return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid token"
        }
        return make_response(jsonify(response_object)), 401


if __name__ == '__main__':
    context = SSL.Context(SSL.SSLv23_METHOD)
    key = os.path.join(os.path.dirname(__file__), '../ssl/private.key')
    cer = os.path.join(os.path.dirname(__file__), '../ssl/self_signed.crt')
    context = (cer, key)

    app.run(host="0.0.0.0",
            port=5000,
            debug=True,
            threaded=True)
