from flask.views import MethodView


class BaseRESTMsg(MethodView):
    url_request = None
    url_response = None
    methods = None
    messenger = None

    def __init__(self):
        # Attributes
        self.accountPrivateId = None
        self.accountPublicId = None
        self.privateId = None
        self.publicId = None
        self.type = None
        self.status = None
        self.creationTime = None
        self.updateTime = None

    def get(self):
        pass

    def post(self):
        pass
