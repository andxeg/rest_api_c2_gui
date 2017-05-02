import time
import json
from flask import jsonify
from flask import request
from flask import make_response
from handlers.account.account_rest_msg import AccountRESTMsg

from handlers.base_response import BaseResponse


class GetAccountInfo(AccountRESTMsg):
    url_request = AccountRESTMsg.url_request + "/get"

    necessary_fields = [
        "method"
    ]

    def __init__(self):
        super(GetAccountInfo, self).__init__()
        self.method = None

    def post(self):
        request_obj = request
        try:
            self._parse_request(request_obj)
        except Exception as e:

            # def __init__(self, request_id=None, code=None, message=None, exception=None):

            response_object = BaseResponse(request_id=self.requestId,
                                           code=str(500),
                                           message=e,
                                           exception=e)

            response_dict = response_object.get_response_dict()

            # response_object = self._create_error_msg(print_info=e,
            #                                          message=e)

            return make_response(jsonify(response_dict)), 500

        print "request-> ", request
        print "request.json -> ", json.dumps(request.json, indent=4, sort_keys=True)

        account = {
            "first_name": "Bob",
            "last_name": "Dylan",
            "id": 1
        }

        if self.method == "short":
            response_object = {
                "account": account
            }

            return make_response(jsonify(response_object)), 200

        elif self.method == "full":
            self._launch_async_handler(self.async_handler, self.request_dict)
            response_object = {
                "status": "processing",
            }
            return make_response(jsonify(response_object)), 200

        else:
            response_object = self._create_error_msg(print_info="GetAccountInfo. Error in field 'method'",
                                                     message="GetAccountInfo. Error in field 'method'")

            return make_response(jsonify(response_object)), 500

    def _parse_request(self, request_obj):
        # raise exception when error in parsing
        # if problem with authentication then return False
        super(GetAccountInfo, self)._parse_request(request_obj)
        self._parse(request_obj)

    def _parse(self, request_obj):
        try:
            self._parse_necessary_fields(self.request_dict,
                                         GetAccountInfo.necessary_fields,
                                         "GetAccountInfo")
        except Exception as e:
            raise

    def async_handler(self, request_dict):
        print "Async processing start"
        account = {
            "first_name": "Bob",
            "last_name": "Dylan",
            "id": 1,
            "email": "bob_dylan@gmail.com",
            "sex": "male",
        }

        time.sleep(10)
        print "Async processing end"

        response_dict = {
            "account": account
        }

        self._send_response(response_dict)
