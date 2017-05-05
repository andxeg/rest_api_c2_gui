import json
from flask import jsonify
from flask import request
from flask import make_response
from handlers.base_rest_msg import BaseRESTMsg


class ServerShutdown(BaseRESTMsg):
    url_request = "shutdown"
    url_response = None
    methods = ['POST']
    messenger = None

    def post(self):
        request_dict = request.json
        if not request_dict:
            response_dict = self._create_error_msg(print_info="Shutdown request has not json format",
                                                   message="Shutdown request has not json format")

            return make_response(jsonify(response_dict)), 500

        try:
            shutdown_token = request_dict["token"]
        except Exception as e:
            print e
            response_dict = self._create_error_msg(print_info="There is not token in request",
                                                   message="There is not token in request")

            return make_response(jsonify(response_dict)), 500

        if shutdown_token == self.messenger.get_shutdown_token():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                print "Not running with the Werkzeug Server"
            func()

            print "Server shutting down"

        response_dict = {
            "token": shutdown_token
        }

        return make_response(jsonify(response_dict)), 200
