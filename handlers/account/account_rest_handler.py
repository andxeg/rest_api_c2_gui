from handlers.base_rest_handler import BaseRESTHandler


class AccountRESTHandler(BaseRESTHandler):
    url_request = "account"
    url_response = None
    methods = None
    messenger = None

    def get(self):
        pass

    def post(self):
        pass
