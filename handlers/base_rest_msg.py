from flask.views import MethodView


class BaseRESTMsg(MethodView):
    url_request = None
    url_response = None
    methods = None
    messenger = None

    def __init__(self):
        # Sender cuuid
        self.senderId = None

        # Attributes
        self.requestId = None
        self.accountPrivateId = None
        self.accountPublicId = None
        self.privateId = None
        self.publicId = None
        self.type = None
        self.status = None
        self.creationTime = None
        self.updateTime = None

        # Auth Manager
        self.auth_manager = self.messenger.get_auth_manager()

    def post(self):
        raise NotImplementedError

    def _parse_request(self, request_obj):

        if self.auth_manager is None:
            return self._simple_parse_base_msg(request_obj)
        else:
            return self._parse_base_msg(request_obj)

        # if parser return false then derived class not needed
        # launch it's own parser. False return when there is
        # problem with authentication
        # If problem with parsing then raise Exception

    def _simple_parse_base_msg(self, request_obj):
        pass

    def _parse_base_msg(self, request_obj):
        # auth_manager = self.messenger.get_auth_manager()
        pass
