from flask import Flask

# TODO. Messenger is singleton or not?


class RESTMessenger(object):
    def __init__(self, server_config=None, client_config=None, async=False):
        self.app = Flask(__name__)
        self.host = server_config.get("host", "127.0.0.1")
        self.port = server_config.get("port", "5000")
        self.debug = server_config.get("debug", False)
        self.response_address = None

        if async:
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

        view_func = class_handler.as_view(str(class_handler.__class__.__name__))
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def print_attributes(self):
        attributes = dir(self)
        for attr_name in attributes:
            attr = getattr(self, attr_name)
            if not callable(attr):
                print "Name -> '%s', Value -> '%s'" % (attr_name, str(attr),)
