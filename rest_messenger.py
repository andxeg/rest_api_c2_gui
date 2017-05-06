import os
import uuid
import json
import requests
from flask import request
from flask import Flask
from OpenSSL import SSL
from handlers.special.server_shutdown import ServerShutdown


# TODO. Messenger is singleton or not?


class RESTMessenger(object):
    def __init__(self, server_config=None, client_config=None, async=False, ssl=False):
        """
            :param server_config: dict 
            :param client_config: dict
            :param async: bool
             If async then messenger can process 
            async requests and config must contain
            notify client's address 
        """

        self.app = Flask(__name__)

        # Need for shutting down
        self.shutdown_token = None

        self.auth_manager = None
        self.host = server_config.get("host", "127.0.0.1")
        self.port = server_config.get("port", "5000")
        self.debug = server_config.get("debug", False)
        # Base url for server. # Full base address ->
        # http:// + host + port + base_url
        self.base_url = server_config.get("base_url", "/")
        self.response_address = None
        self.context = None

        # Need for sending request to remote client
        self.verify_crt_path = None

        self.__set_verify_certificate(client_config)

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

    def run(self, threaded=False):
        self.app.run(host=self.host,
                     port=self.port,
                     debug=self.debug,
                     ssl_context=self.context,
                     threaded=threaded)

    def get_shutdown_token(self):
        result = None
        field = "shutdown_token"
        if hasattr(self, field):
            result = getattr(self, field)

        return result

    def terminate(self):
        # TODO terminate rest messenger
        # TODO First server stops to receive messages
        # TODO Second wait all threads will be terminate
        # TODO Third terminate rest

        # Terminate server
        self.shutdown_token = str(uuid.uuid4())
        print self.shutdown_token

        self.add_handler(ServerShutdown.url_request, ServerShutdown, ServerShutdown.methods, async=False)

        verify = False
        prefix = "http://"

        if self.context is not None:
            prefix = "https://"
            verify = self.context[0]
        
        shutdown_url = prefix + self.host + ':' + self.port + self.base_url + '/' + ServerShutdown.url_request

        request_dict = {
            "token": self.shutdown_token
        }

        response = requests.post(shutdown_url, json=request_dict, verify=verify)
        response_dict = response.json()
        try:
            if response_dict and response_dict["token"] == self.shutdown_token:
                return
        except Exception as e:
            print e
            print "Server is still running"

    def print_attributes(self):
        attributes = dir(self)
        for attr_name in attributes:
            attr = getattr(self, attr_name)
            if not callable(attr):
                print "Name -> '%s', Value -> '%s'" % (attr_name, str(attr),)

    def __set_verify_certificate(self, client_config):
        try:
            ssl = client_config["ssl"]
            if "verify" in ssl:
                self.verify_crt_path = os.path.dirname(os.path.abspath(__file__)) + '/' + ssl["verify"]
        except KeyError as e:
            import traceback
            traceback.print_exc()
            raise Exception("error '%s' while read verify certificate path" % (e,))

    def __set_notify_address(self, client_config):
        try:
            prefix = "http://"
            if self.verify_crt_path:
                prefix = "https://"

            notify = prefix + \
                     client_config["host"] + ':' + \
                     client_config["port"] + '/' + \
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

    def get_verify_crt(self):
        if self.verify_crt_path:
            return self.verify_crt_path

        return False
