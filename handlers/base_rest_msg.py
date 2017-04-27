from flask import jsonify
from flask import request
from flask import make_response
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

    @classmethod
    def _create_error_msg(cls, print_info=None, message=None):
        print str(print_info)

        error_msg = {
            "status": "fail",
            "message": str(message)
        }

        return error_msg

    def _parse_request(self, request_obj):

        if self.auth_manager is None:
            return self._simple_parse_base_msg(request_obj)
        else:
            return self._parse_base_msg(request_obj)

    # if parser return false then derived class not needed
    # launch it's own parser. False return when there is
    # problem with authentication
    # If problem with parsing then raise Exception
    # Exception catch the highest class in hierarchy

    def _simple_parse_base_msg(self, request_obj):
        print request_obj
        print "There is not auth manager in REST messenger."
        return False

    def _parse_base_msg(self, request_obj):
        request_dict = request_obj.json
        if not request_dict:
            raise Exception("Request has not a json format")

        if "requestId" not in request_dict:
            raise Exception("Request has not a json format")



