from flask import jsonify
from flask import request
from flask import make_response
from flask.views import MethodView


class BaseRESTMsg(MethodView):
    url_request = None
    url_response = None
    methods = None
    messenger = None

    necessary_fields = [
        "requestId"
    ]

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

        # Request dict
        self.request_dict = None

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

    def print_attributes(self):
        attributes = self.__dict__
        for attribute, value in attributes.items():
            print "'%s' -> '%s'" % (str(attribute), str(value))

    def _parse_request(self, request_obj):
        if self.auth_manager is None:
            self._simple_parse_base_msg(request_obj)
        else:
            self._parse_base_msg(request_obj)

    # If problem with parsing or with authentication
    # then raise Exception. Exception catch the
    # highest class in hierarchy.

    @staticmethod
    def _simple_parse_base_msg(request_obj):
        print request_obj
        raise Exception("BaseRESTMsg. There is not auth manager in REST messenger.")

    def __check_auth_token(self, request_obj):
        auth_header = request_obj.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if not auth_token:
            raise Exception("BaseRESTMsg. There is not an authentication token in request.")

        user_id, error = self.auth_manager.decode_auth_token(auth_token)

        if error is not None:
            raise Exception(error)

        user = self.auth_manager.find_user_by_id(user_id)

        if user is None:
            raise Exception("BaseRESTMsg. There is not user with such token.")

        self.senderId = user_id

    def _parse_necessary_fields(self, request_dict, necessary_fields, handler_name):
        for field in necessary_fields:
            if field not in request_dict:
                raise Exception("%s. Request has't necessary field '%s'" % (field, handler_name))

            field_value = request_dict[field]

            if not hasattr(self, field):
                raise Exception("%s hasn't field with name '%s'" % (field, handler_name))

            try:
                setattr(self, field, field_value)
            except Exception as e:
                print e
                raise Exception("%s. Problem with setattr method." % (handler_name,))

    def _parse_base_msg(self, request_obj):
        # if application/json then json else None
        self.request_dict = request_obj.json

        # TODO. Parsing may do using attributes,
        # TODO. so without such a lot of if operators
        # TODO. Parsing may do using special dict or list with
        # TODO. necessary fields

        if not self.request_dict:
            raise Exception("Request hasn't a json")

        try:
            self.__check_auth_token(request_obj)
        except Exception as e:
            raise

        try:
            self._parse_necessary_fields(self.request_dict,
                                         BaseRESTMsg.necessary_fields,
                                         "BaseRestMsg")
        except Exception as e:
            raise
