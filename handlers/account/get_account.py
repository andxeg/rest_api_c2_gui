import json
from flask import jsonify
from flask import request
from flask import make_response
from handlers.account.account_rest_msg import AccountRESTMsg


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
            response_object = self._create_error_msg(print_info=e,
                                                     message=e)

            return make_response(jsonify(response_object)), 500

        print "request-> ", request
        print "request.json -> ", json.dumps(request.json, indent=4, sort_keys=True)

        account = {
            "first_name": "Bob",
            "last_name": "Dylan",
            "id": 1
        }

        if self.method == "short":
            pass
        elif self.method == "full":
            account["email"] = "bob_dylan@gmail.com"
            account["sex"] = "male"
        else:
            response_object = self._create_error_msg(print_info="Error in field 'method'",
                                                     message="Error in field 'method'")

            return make_response(jsonify(response_object)), 500

        response_object = {
            "account": account
        }

        return make_response(jsonify(response_object)), 200

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
