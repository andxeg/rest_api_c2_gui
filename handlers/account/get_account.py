from flask import jsonify
from handlers.account.account_rest_handler import AccountRESTHandler


class GetAccountInfo(AccountRESTHandler):
    url_request = AccountRESTHandler.url_request + "/get"
    url_response = None
    methods = None
    messenger = None

    def get(self):
        account = {
            "firstname": "Andrew",
            "lastname": "Chupakhin",
            "id": 1
        }
        return jsonify({'account': account})

    def post(self):
        pass
