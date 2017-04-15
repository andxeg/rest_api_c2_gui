import json
from flask import jsonify
from flask import request
from handlers.service.service_rest_msg import ServiceRESTMsg


class FunctionDescription(ServiceRESTMsg):
    url_request = ServiceRESTMsg.url_request + "/function"

    def __init__(self):
        super(FunctionDescription, self).__init__()

    def post(self):
        pass

    def _parse_request(self, request_obj):
        try:
            result = super(FunctionDescription, self)._parse_request(request_obj)
        except Exception as e:
            print e
            return False

        if result:
            return self._parse(request_obj)
        else:
            return False

    def _parse(self, request_obj):
        pass
