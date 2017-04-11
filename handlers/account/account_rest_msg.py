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

    def get(self):
        pass

    def post(self):
        pass
