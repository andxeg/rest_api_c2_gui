from flask import Flask, jsonify
from flask import abort, make_response
from flask import request
from flask import url_for

from flask_httpauth import HTTPBasicAuth

import os
import time
from md5 import md5

from OpenSSL import SSL

app = Flask(__name__)
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
    "andrew": "202cb962ac59075b964b07152d234b70",
    "test":   "81dc9bdb52d04dc20036dbd8313ed055"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
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

if __name__ == '__main__':
    context = SSL.Context(SSL.SSLv23_METHOD)
    key = os.path.join(os.path.dirname(__file__), '../ssl/private.key')
    cer = os.path.join(os.path.dirname(__file__), '../ssl/self_signed.crt')
    context = (cer, key)
    app.run(host="0.0.0.0",
            port=5000,
            debug=True,
            threaded=True,
            ssl_context=context)
