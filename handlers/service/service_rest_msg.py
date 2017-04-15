from handlers.base_rest_msg import BaseRESTMsg


class ServiceRESTMsg(BaseRESTMsg):
    url_request = "service"
    methods = ['POST']

    def __init__(self):
        super(ServiceRESTMsg, self).__init__()
        # Characteristics

    def post(self):
        pass

    def _parse_request(self, request_obj):
        try:
            result = super(ServiceRESTMsg, self)._parse_request(request_obj)
        except Exception as e:
            print e
            return False

        if result:
            return self._parse_service_msg(request_obj)
        else:
            return result

    def _parse_service_msg(self, request_obj):
        pass
