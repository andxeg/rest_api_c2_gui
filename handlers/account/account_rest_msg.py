from handlers.base_rest_msg import BaseRESTMsg


class AccountRESTMsg(BaseRESTMsg):
    url_request = "account"
    methods = ['POST']

    necessary_fields = [
        "type",
        "accountPublicId",
        "accountPrivateId",
        "privateId",
        "publicId"
    ]

    def __init__(self):
        super(AccountRESTMsg, self).__init__()
        '''
        Attributes 
        type == Account
        accountPublicId == publicId
        accountPrivateId == privateId
        '''

        # Characteristics
        self.password = None
        self.tag1 = None
        self.tag2 = None
        self.tag1_type = None
        self.tag2_type = None
        self.remoteIp = None
        self.externalIp = None

    def post(self):
        raise NotImplementedError

    def _parse_request(self, request_obj):
        # raise exception when error in parsing
        # if problem with authentication then also raise exception
        super(AccountRESTMsg, self)._parse_request(request_obj)
        self._parse_account_msg(request_obj)

    def _parse_account_msg(self, request_obj):
        if "attributes" not in self.request_dict:
            raise Exception("AccountRESTMsg. There is not field 'attributes' in request.")

        attributes = self.request_dict["attributes"]
        try:
            self._parse_necessary_fields(attributes,
                                         AccountRESTMsg.necessary_fields,
                                         "AccountRESTMsg")
        except Exception as e:
            raise
