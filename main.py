import os
from config import Config
from rest_messenger import RESTMessenger
from handlers.test_handlers.tasks_lists import TasksList
from handlers.account.get_account import GetAccountInfo
from auth.auth_manager import AuthManager
from auth.login_msg import LoginRESTMsg
from auth.logout_msg import LogoutRESTMsg


CONFIG_FILE = "rest_config.json"


def add_handlers(messenger):
    messenger.add_handler(TasksList.url_request, TasksList, TasksList.methods, async=True)
    messenger.add_handler(GetAccountInfo.url_request, GetAccountInfo, GetAccountInfo.methods, async=False)


if __name__ == '__main__':
    # TODO RESTMessenger go into infinite loop
    # TODO If you want to use it you must launch messenger in thread

    # TODO may be for requests create appropriate classes
    # GUI server while work as web server and don't make large requests

    curr_dir_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    config_file_path = curr_dir_path + CONFIG_FILE
    config = Config(config_file_path)
    config.read_config()
    c2_config_dict = config.get_sub_config_by_key("c2_config")
    oss_bss_config_dict = config.get_sub_config_by_key("oss_bss_config")

    rest_messenger = RESTMessenger(server_config=c2_config_dict,
                                   client_config=oss_bss_config_dict,
                                   async=True,
                                   ssl=True)

    rest_messenger.print_attributes()
    add_handlers(rest_messenger)

    auth_manager = AuthManager()
    handler_list = [LoginRESTMsg, LogoutRESTMsg]
    auth_manager.add_handler_list(handler_list)
    rest_messenger.set_auth_manager(auth_manager)

    rest_messenger.run()

    print "FINISH"
