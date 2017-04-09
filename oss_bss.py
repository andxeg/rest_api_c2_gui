import os
import requests
from config import Config
from rest_messenger import RESTMessenger
from handlers.test_handlers.notify_handler import NotifyHandler

CONFIG_FILE = "oss_bss_config.json"
C2_ADDRESS = "http://0.0.0.0:5007/todo/api/v1.0/tasks"
MODULE_NAME = "OSS_BSS"


def add_handlers(messenger):
    messenger.add_handler(NotifyHandler.url_request,
                          NotifyHandler,
                          NotifyHandler.methods,
                          async=False)


if __name__ == '__main__':
    curr_dir_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    config_file_path = curr_dir_path + CONFIG_FILE
    config = Config(config_file_path)
    config.read_config()
    c2_config_dict = config.get_sub_config_by_key("c2_config")
    oss_bss_config_dict = config.get_sub_config_by_key("oss_bss_config")

    rest_messenger = RESTMessenger(server_config=oss_bss_config_dict,
                                   client_config=c2_config_dict,
                                   async=False)

    rest_messenger.print_attributes()
    add_handlers(rest_messenger)

    # send request to server
    data = {
        "title": "Read a book"
    }

    print("%s | Before send request to '%s'" % (MODULE_NAME, C2_ADDRESS))
    response = requests.post(C2_ADDRESS, json=data)
    print("%s | Receive ack from '%s'" % (MODULE_NAME, C2_ADDRESS))

    rest_messenger.run()
