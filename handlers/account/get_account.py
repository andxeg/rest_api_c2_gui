import json
from flask import jsonify
from flask import request
from handlers.account.account_rest_msg import AccountRESTMsg


class GetAccountInfo(AccountRESTMsg):
    url_request = AccountRESTMsg.url_request + "/get"

    def __init__(self):
        super(GetAccountInfo, self).__init__()

    def get(self):
        pass

    def post(self):
        print "request-> ", request
        print "request.json -> ", json.dumps(request.json, indent=4, sort_keys=True)
        account = {
            "first_name": "Andrew",
            "last_name": "Chupakhin",
            "id": 1
        }
        return jsonify({'account': account})
