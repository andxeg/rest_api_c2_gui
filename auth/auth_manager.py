

class AuthManager(object):
    def __init__(self):
        self.handlers = []

    def get_handlers(self):
        pass

    def append_handler(self, handler):
        self.handlers.append(handler)

    def check_token(self):
        pass
