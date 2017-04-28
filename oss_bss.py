import os

import requests

from config.config import Config
from handlers.test_handlers.notify_handler import NotifyMsg
from rest_messenger import RESTMessenger

CONFIG_FILE = "./config/oss_bss_config.json"
C2_ADDRESS = "https://0.0.0.0:5007/todo/api/v1.0/tasks"
MODULE_NAME = "OSS_BSS"


def add_handlers(messenger):
    messenger.add_handler(NotifyMsg.url_request,
                          NotifyMsg,
                          NotifyMsg.methods,
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
                                   async=False,
                                   ssl=False)

    rest_messenger.print_attributes()
    add_handlers(rest_messenger)

    # send request to server
    data = {
        "title": "Read a book"
    }

    print("%s | Before send request to '%s'" % (MODULE_NAME, C2_ADDRESS))
    verify = oss_bss_config_dict["ssl"]["verify"]
    response = requests.post(C2_ADDRESS, json=data, verify=verify)
    print("%s | Receive ack from '%s'" % (MODULE_NAME, C2_ADDRESS))

    rest_messenger.run(threaded=True)

    print "FINISH"
