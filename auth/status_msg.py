from flask import jsonify
from flask import request
from flask import make_response
from auth.base_auth_msg import BaseAuthMsg


class StatusRESTMsg(BaseAuthMsg):
    url_request = BaseAuthMsg.url_request + "/status"

    def post(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            if self.auth_manager is None:
                response_object = self.create_error_msg(print_info="There is not auth manager in REST messenger.",
                                                        message="Auth is not available now")
                return make_response(jsonify(response_object)), 500

            user_id, error = self.auth_manager.decode_auth_token(auth_token)

            if error is not None:
                response_object = self.create_error_msg(print_info=error,
                                                        message=error)
                return make_response(jsonify(response_object)), 500

            user = self.auth_manager.find_user_by_id(user_id)

            if user is None:
                response_object = self.create_error_msg(print_info="There is not auth manager in REST messenger.",
                                                        message="User was not found")
                return make_response(jsonify(response_object)), 200

            response_object = {
                "status": "success",
                "data": {
                    "email": str(user["email"]),
                    "name": str(user["name"])
                }
            }
            return make_response(jsonify(response_object)), 200

        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid auth token"
            }
            return make_response(jsonify(response_object)), 403
