from flask import request
from flask import jsonify
from handlers.account.account_rest_msg import AccountRESTMsg


class CreateAccount(AccountRESTMsg):
    url_request = AccountRESTMsg.url_request + "/create"

    def __init__(self):
        super(CreateAccount, self).__init__()

    def post(self):
        # receive post request

        # check request json

        # if error send response with error

        pass

    def error_handler(self):
        pass

    def parse_request(self, request_dict):
        pass

    # def post(self):
    #     print('%s | Receive post request' % MODULE_NAME)
    #     if not request.json or 'title' not in request.json:
    #         abort(400)
    #
    #     print('%s | Sending ack on post request' % MODULE_NAME)
    #     return jsonify({'status': 'processing'})
