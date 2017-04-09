from flask.views import MethodView


class BaseRESTHandler(MethodView):
    url_request = None
    url_response = None
    methods = None
    messenger = None

    def get(self):
        pass

    def post(self):
        pass
