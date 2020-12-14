from flask import Flask
from flask_kerberos import requires_authentication
from flask_kerberos import init_kerberos

app = Flask(__name__)
init_kerberos(app, hostname='test_sso.com')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/protected")
@requires_authentication
def protected_view(user):
    return "你成功的访问我了。"

