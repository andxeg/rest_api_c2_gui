from flask.views import MethodView


class BaseAuthMsg(MethodView):
    url_request = "auth"
    url_response = None
    methods = ['POST']
    messenger = None

    def __init__(self):
        self.auth_manager = self.messenger.get_auth_manager()

    def post(self):
        pass

    @classmethod
    def create_error_msg(cls, print_info=None, message=None):
        print str(print_info)

        error_msg = {
            "status": "fail",
            "message": str(message)
        }

        return error_msg
