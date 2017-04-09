# # EXAMPLE HANDLER FOR OSS BSS

from flask import jsonify
from flask import request
from flask.views import MethodView
import json

MODULE_NAME = "OSS_BSS"


class NotifyHandler(MethodView):
    url_response = None
    url_request = "/oss_bss/notify"
    methods = ['POST']

    def post(self):
        print('%s | Receive post request' % MODULE_NAME)
        print json.dumps(request.json, indent=4, sort_keys=True)
        print('%s | Sending response on post request' % MODULE_NAME)
        return jsonify({'status': 'all ok'})
