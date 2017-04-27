from handlers.base_rest_msg import BaseRESTMsg


class AccountRESTMsg(BaseRESTMsg):
    url_request = "account"
    methods = ['POST']

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
        try:
            result = super(AccountRESTMsg, self)._parse_request(request_obj)
        except Exception as e:
            print e
            raise

        if not result:
            return False

        return self._parse_account_msg(request_obj)

    def _parse_account_msg(self, request_obj):
        pass
