import time
import threading
import requests
import copy

from flask import Flask, jsonify
from flask import abort, make_response
from flask import request
from flask.views import MethodView

FLASK_APP_CONFIG = {
    'host': "0.0.0.0",
    'port': "5000",
    'debug': False,
}

ASYNC_REQUEST_ADDRESS = "http://0.0.0.0:5001/oss_bss/notify"
MODULE_NAME = "SERVER"

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


class TasksList(MethodView):

    # get tasks
    def get(self):
        print('%s | Receive get request' % MODULE_NAME)
        return jsonify({'tasks': tasks})

    # create task
    def post(self):
        print('%s | Receive post request' % MODULE_NAME)
        if not request.json or 'title' not in request.json:
            abort(400)

        # TODO launch thread for request processing
        req = copy.deepcopy(dict(request.json))
        thread = threading.Thread(target=self.async_handler, args=(req,))
        thread.setDaemon(True)
        thread.start()

        time.sleep(1)
        print('%s | Sending response on post request' % MODULE_NAME)
        return jsonify({'status': 'processing'})

    def async_handler(self, req):

        task = {
            'id': tasks[-1]['id'] + 1,
            'title': req['title'],
            'description': req.get('description', ""),
            'done': False,
        }

        tasks.append(task)

        print('%s | Async processing start' % MODULE_NAME)
        time.sleep(5)
        print('%s | Async processing end' % MODULE_NAME)

        print('%s | Sending request to %s' % (MODULE_NAME, ASYNC_REQUEST_ADDRESS))
        data = {'status': 'Done', 'task': task}
        response = requests.post(ASYNC_REQUEST_ADDRESS, json=data)
        print('%s | Receive response from %s' % (MODULE_NAME, ASYNC_REQUEST_ADDRESS))
        print(response.json())

        return


class RESTMessenger(object):
    def __init__(self):
        self.app = Flask(__name__)

    def add_handler(self, rule, class_handler, methods):
        view_func = class_handler.as_view(str(class_handler.__class__.__name__))
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def run(self, host="127.0.0.1", port="5000", debug=False):
        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # TODO Server must launch messenger in thread
    rest_messenger = RESTMessenger()
    rest_messenger.add_handler('/todo/api/v1.0/tasks', TasksList, methods=['GET', 'POST'])
    rest_messenger.run(FLASK_APP_CONFIG['host'],
                       FLASK_APP_CONFIG['port'],
                       FLASK_APP_CONFIG['debug'],)
