import time
from handlers.account.account_response import AccountResponse


#   This class implement account response message.
#   All type of response consists of:
#   1. HTTP code of response message
#   2. baseResponse structure with timestamp, error code, message and exception
#   3. Other payload information


class GetAccountResponse(AccountResponse):
    def __init__(self,
                 request_id=None,
                 code=None,
                 message=None,
                 exception=None,
                 account_private_id=None,
                 account_public_id=None,
                 status=None,
                 creation_time=None,
                 update_time=None,
                 password=None,
                 tag1=None,
                 tag2=None,
                 tag1_type=None,
                 tag2_type=None,
                 remote_ip=None,
                 external_ip=None):

        super(GetAccountResponse, self).__init__(request_id=request_id,
                                                 code=code,
                                                 message=message,
                                                 exception=exception,
                                                 account_private_id=account_private_id,
                                                 account_public_id=account_public_id,
                                                 status=status,
                                                 creation_time=creation_time,
                                                 update_time=update_time)
        self.characteristics = {}

        self.password = password
        self.tag1 = tag1
        self.tag2 = tag2
        self.tag1_type = tag1_type
        self.tag2_type = tag2_type
        self.remoteIp = remote_ip
        self.externalIp = external_ip

    # All derived classes first call
    # 'make_response' from base class
    # then call own 'make_response'
    # after that you can call get_response_dict
    def _make_response(self):
        super(GetAccountResponse, self)._make_response()

        # Create characteristics structure
        self.characteristics["password"] = self.password
        self.characteristics["tag1"] = self.tag1
        self.characteristics["tag2"] = self.tag2
        self.characteristics["tag1_type"] = self.tag1_type
        self.characteristics["tag2_type"] = self.tag2_type
        self.characteristics["remoteIp"] = self.remoteIp
        self.characteristics["externalIp"] = self.externalIp

        # Add characteristics to response dict
        self.response_dict["characteristics"] = self.characteristics
