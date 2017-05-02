import json
import os

import copy
import random
import requests

from config.config import Config
from handlers.test_handlers.notify_handler import NotifyMsg
from rest_messenger import RESTMessenger

CONFIG_FILE = "./config/oss_bss_config.json"
C2_ADDRESS = "https://0.0.0.0:5007/todo/api/v1.0"
MODULE_NAME = "OSS_BSS"

C2_ADD_TASK = C2_ADDRESS + "/tasks"
C2_LOGIN = C2_ADDRESS + "/auth/login"
C2_LOGOUT = C2_ADDRESS + "/auth/logout"
C2_GET_ACCOUNT_INFO = C2_ADDRESS + "/account/get"


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

    # rest_messenger.print_attributes()
    add_handlers(rest_messenger)

    verify = oss_bss_config_dict["ssl"]["verify"]

    # Authentication. Get token from server
    data = {
        "name": "admin",
        "password": "admin"
    }

    print("%s | Before send request to '%s'" % (MODULE_NAME, C2_LOGIN))
    response = requests.post(C2_LOGIN, json=data, verify=verify)
    response_dict = response.json()
    auth_token = response_dict.get("auth_token", "")
    print("%s | Receive response from '%s'" % (MODULE_NAME, C2_LOGIN))

    # Send async request for GetAccountInfo message
    data = {
        "requestId": "1234",
        "attributes": {
            "type": "type",
            "accountPublicId": "accountPublicId",
            "accountPrivateId": "accountPrivateId",
            "privateId": "privateId",
            "publicId": "publicId"
        },
        "method": "full"
    }

    msg_count = 1
    data_set = []
    methods = ["short", "full"]
    for i in range(msg_count):
        data["method"] = methods[random.randint(0, 1)]
        data_set.append(copy.deepcopy(data))

    for d in data_set:
        print json.dumps(d, indent=4, sort_keys=True)

    for msg in data_set:
        print("%s | Before send request to '%s'" % (MODULE_NAME, C2_GET_ACCOUNT_INFO))
        response = requests.post(C2_GET_ACCOUNT_INFO,
                                 json=msg,
                                 verify=verify,
                                 headers={
                                     "Authorization": "Bearer " + auth_token
                                 })

        print("%s | Receive ack from '%s'" % (MODULE_NAME, C2_GET_ACCOUNT_INFO))
        print json.dumps(response.json(), indent=4, sort_keys=True)

    rest_messenger.run(threaded=True)

    print "FINISH"
