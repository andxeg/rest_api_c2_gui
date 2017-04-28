from flask import jsonify
from flask import request
from flask import make_response
from auth.base_auth_msg import BaseAuthMsg


class LoginRESTMsg(BaseAuthMsg):
    url_request = BaseAuthMsg.url_request + "/login"

    def post(self):
        request_dict = request.json
        try:
            name = request_dict.get("name", "")
            password = request_dict.get("password", "")

            if self.auth_manager is None:
                response_object = self.create_error_msg(print_info="There is not auth manager in REST messenger.",
                                                        message="Auth is not available now")
                return make_response(jsonify(response_object)), 500

            user_id = self.auth_manager.check_password(name, password)

            if user_id is None:
                response_object = self.create_error_msg(print_info="User or password are incorrect",
                                                        message="User or password are incorrect")
                return make_response(jsonify(response_object)), 404

            auth_token = self.auth_manager.encode_auth_token(user_id)

            if auth_token is None:
                response_object = self.create_error_msg(print_info="Error in token encoding",
                                                        message="Error in token encoding")
                return make_response(jsonify(response_object)), 404

            response_object = {
                "status": "success",
                "message": "Successfully logged in",
                "auth_token": auth_token.decode()
            }
            return make_response(jsonify(response_object)), 200

        except Exception as e:
            response_object = self.create_error_msg(print_info=e,
                                                    message=e)
            return make_response(jsonify(response_object)), 500
