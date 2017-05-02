import time
from handlers.base_response import BaseResponse


#   This class implement account response message.
#   All type of response consists of:
#   1. HTTP code of response message
#   2. baseResponse structure with timestamp, error code, message and exception
#   3. Other payload information


class AccountResponse(BaseResponse):
    def __init__(self,
                 request_id=None,
                 code=None,
                 message=None,
                 exception=None,
                 account_private_id=None,
                 account_public_id=None,
                 status=None,
                 creation_time=None,
                 update_time=None):

        super(AccountResponse, self).__init__(request_id=request_id,
                                              code=code,
                                              message=message,
                                              exception=exception)
        self.attributes = {}

        self.accountPrivateId = str(account_private_id)
        self.accountPublicId = str(account_public_id)
        self.type = "ACCOUNT"
        self.status = str(status)
        self.creationTime = str(creation_time)
        self.updateTime = str(update_time)

    # All derived classes first call
    # 'make_response' from base class
    # then call own 'make_response'
    # after that you can call get_response_dict
    def _make_response(self):
        super(AccountResponse, self)._make_response()

        # Create attributes structure
        self.attributes["accountPrivateId"] = self.accountPrivateId
        self.attributes["accountPublicId"] = self.accountPublicId
        self.attributes["privateId"] = self.accountPrivateId
        self.attributes["publicId"] = self.accountPublicId
        self.attributes["type"] = self.type
        self.attributes["status"] = self.status
        self.attributes["creationTime"] = self.creationTime
        self.attributes["updateTime"] = self.updateTime

        # Add attributes to response dict
        self.response_dict["attributes"] = self.attributes
