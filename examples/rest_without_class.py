from flask import Flask, jsonify
from flask import abort, make_response
from flask import request
from flask import url_for
from flask.views import MethodView
import time

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


class RequestHandler(MethodView):
    def handle(self):
        return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app=Flask(__name__)
    app.add_url_rule('/todo/api/v1.0/tasks', view_func=RequestHandler.as_view('request_handler'))
    app.run()


