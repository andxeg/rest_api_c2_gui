import time


#   This class implement base response message.
#   All type of response consists of:
#   1. HTTP code of response message
#   2. baseResponse structure with timestamp, error code, message and exception
#   3. Other payload information


class BaseResponse(object):
    def __init__(self,
                 request_id=None,
                 code=None,
                 message=None,
                 exception=None):

        self.response_dict = {}
        self.requestId = request_id
        self.baseResponse = {}
        self.code = str(code)
        self.message = str(message)
        self.exception = str(exception)
        self.timestamp = None

    # All derived classes first call
    # 'make_response' from base class
    # then call own 'make_response'
    # after that you can call get_response_dict
    def _make_response(self):
        # Add request id
        self.response_dict["requestId"] = self.requestId

        # Create base response structure
        self.baseResponse["code"] = self.code
        self.baseResponse["message"] = self.message
        self.baseResponse["exception"] = self.exception
        self.baseResponse["timestamp"] = str(int(time.time()))

        # Add base response structure
        self.response_dict["baseResponse"] = self.baseResponse

    def get_response_dict(self):
        self._make_response()
        return self.response_dict
