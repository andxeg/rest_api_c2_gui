from flask import Flask
from flask_httpauth import HTTPBasicAuth
from md5 import md5

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    'alice': "202cb962ac59075b964b07152d234b70", # '123'
    'bob':   "81dc9bdb52d04dc20036dbd8313ed055"  # '1234'
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()


@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run()