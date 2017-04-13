from handlers.base_rest_msg import BaseRESTMsg


class ServiceRESTMsg(BaseRESTMsg):
    url_request = "service"
    methods = ['POST']

    def __init__(self):
        super(ServiceRESTMsg, self).__init__()
        # Characteristics

    def post(self):
        pass
