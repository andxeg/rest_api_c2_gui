# EXAMPLE HANDLER FOR SERVER

import json
import time
import threading
import requests
import copy

from flask import jsonify
from flask import abort
from flask import request
from handlers.base_rest_msg import BaseRESTMsg

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


class TasksList(BaseRESTMsg):
    url_request = "tasks"
    methods = ['GET', 'POST']

    # Synchronous message
    # get tasks
    def get(self):
        print('%s | Receive get request' % MODULE_NAME)
        return jsonify({'tasks': tasks})

    # Asynchronous message
    # create task
    def post(self):
        print('%s | Receive post request' % MODULE_NAME)
        if not request.json or 'title' not in request.json:
            abort(400)

        # TODO launch thread for request processing
        request_dict = copy.deepcopy(dict(request.json))
        thread = threading.Thread(target=self.async_handler, args=(request_dict,))
        thread.setDaemon(True)
        thread.start()

        print('%s | Sending ack on post request' % MODULE_NAME)
        return jsonify({'status': 'processing'})

    def async_handler(self, request_dict):

        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request_dict['title'],
            'description': request_dict.get('description', ""),
            'done': False,
        }

        tasks.append(task)

        print('%s | Async processing start' % MODULE_NAME)
        time.sleep(5)
        print('%s | Async processing end' % MODULE_NAME)

        print('%s | Sending request to %s' % (MODULE_NAME, self.url_response))
        data = {'status': 'Done', 'task': task}

        response = requests.post(self.url_response, json=data)

        print('%s | Receive ack from %s' % (MODULE_NAME, self.url_response))
        print json.dumps(response.json(), indent=4, sort_keys=True)

        self.messenger.print_attributes()

        return
