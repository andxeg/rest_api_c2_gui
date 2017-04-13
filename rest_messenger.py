import os
from flask import Flask
from OpenSSL import SSL

# TODO. Messenger is singleton or not?


class RESTMessenger(object):
    def __init__(self, server_config=None, client_config=None, async=False, ssl=False):
        '''
            :param server_config: dict 
            :param client_config: dict
            :param async: bool 
            If async then messenger can process 
            async requests and config must contain
            notify client's address 
        '''

        self.app = Flask(__name__)
        self.auth_manager = None
        self.host = server_config.get("host", "127.0.0.1")
        self.port = server_config.get("port", "5000")
        self.debug = server_config.get("debug", False)
        # Base url for server. # Full base address ->
        # http:// + host + port + base_url
        self.base_url = server_config.get("base_url", "/")
        self.response_address = None
        self.context = None

        if async is True:
            self.__set_notify_address(client_config)

        if ssl is True:
            ssl_config = server_config.get("ssl", None)
            self.__set_ssl_context(ssl_config)

    def add_handler(self, rule, class_handler, methods, url_response=None, async=True):
        if async:
            if url_response is not None:
                # custom url_response
                class_handler.url_response = url_response
            elif self.response_address is not None:
                # default url_response from config
                class_handler.url_response = self.response_address
            else:
                raise Exception("async handler has not url for response")

        class_handler.messenger = self
        view_func = class_handler.as_view(str(class_handler.__name__))
        handler_url = self.base_url + '/' + rule
        self.app.add_url_rule(handler_url,
                              view_func=view_func,
                              methods=methods)

    def run(self):
        self.app.run(host=self.host,
                     port=self.port,
                     debug=self.debug,
                     ssl_context=self.context)

    def print_attributes(self):
        attributes = dir(self)
        for attr_name in attributes:
            attr = getattr(self, attr_name)
            if not callable(attr):
                print "Name -> '%s', Value -> '%s'" % (attr_name, str(attr),)

    def __set_notify_address(self, client_config):
        try:
            notify = "http://" + \
                     client_config["host"] + \
                     ':' + \
                     client_config["port"] + \
                     '/' + \
                     client_config["notify"]
        except KeyError as e:
            import traceback
            traceback.print_exc()
            raise Exception("error '%s' while read notify address" % (e,))

        self.response_address = notify

    def __set_ssl_context(self, server_config):
        self.context = SSL.Context(SSL.SSLv23_METHOD)
        try:
            private_key = server_config["key"]
            certificate = server_config["crt"]
            # TODO Add check existence of this files
            # TODO
            key = os.path.join(os.path.dirname(__file__), private_key)
            cer = os.path.join(os.path.dirname(__file__), certificate)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception("Cannot find files with key and certificate. "
                            "Exception '%s'" % (e,))

        self.context = (cer, key)

    def get_auth_manager(self):
        return self.auth_manager

    def set_auth_manager(self, auth_manager):
        self.auth_manager = auth_manager
        handlers = self.auth_manager.get_handlers()
        for handler in handlers:
            self.add_handler(handler.url_request, handler, handler.methods, async=False)
