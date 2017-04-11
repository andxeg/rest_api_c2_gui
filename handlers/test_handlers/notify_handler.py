# # EXAMPLE HANDLER FOR OSS BSS

import json
from flask import jsonify
from flask import request
from handlers.base_rest_msg import BaseRESTMsg


MODULE_NAME = "OSS_BSS"


class NotifyMsg(BaseRESTMsg):
    url_request = "oss_bss/notify"
    methods = ['POST']

    def post(self):
        print('%s | Receive post request' % MODULE_NAME)
        print json.dumps(request.json, indent=4, sort_keys=True)
        print('%s | Sending ack on post request' % MODULE_NAME)
        return jsonify({'status': 'all ok'})
