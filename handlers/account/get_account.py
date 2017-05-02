import time
import json
from flask import jsonify
from flask import request
from flask import make_response
from handlers.account.account_rest_msg import AccountRESTMsg

from handlers.base_response import BaseResponse
from handlers.account.get_account_response import GetAccountResponse


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

            return make_response(jsonify(response_dict)), 500

        print "request-> ", request
        print "request.json -> ", json.dumps(request.json, indent=4, sort_keys=True)

        account = {
            "first_name": "Bob",
            "last_name": "Dylan",
            "id": 1
        }

        if self.method == "short":
            # response_object = {
            #     "account": account
            # }

            # TODO Take this info from database
            creation_time = int(time.time()) - 1000
            update_time = int(time.time()) - 1000
            password = "password"
            tag1 = 123456
            tag2 = 1000
            tag1_type = "VXLAN"
            tag2_type = "VLAN"
            remote_ip = "1.1.1.1"
            external_ip = "4.4.4.4"

            response_object = GetAccountResponse(request_id=self.requestId,
                                                 code=200,
                                                 message=None,
                                                 exception=None,
                                                 account_private_id=self.accountPrivateId,
                                                 account_public_id=self.accountPublicId,
                                                 status="ACTIVE",
                                                 creation_time=str(creation_time),
                                                 update_time=str(update_time),
                                                 password=password,
                                                 tag1=str(tag1),
                                                 tag2=str(tag2),
                                                 tag1_type=tag1_type,
                                                 tag2_type=tag2_type,
                                                 remote_ip=remote_ip,
                                                 external_ip=external_ip)

            response_dict = response_object.get_response_dict()

            return make_response(jsonify(response_dict)), 200

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
