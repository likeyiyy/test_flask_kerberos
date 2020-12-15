from flask import Flask
from flask_kerberos import init_kerberos, requires_authentication

app = Flask(__name__)
init_kerberos(app, hostname='webserver.example.com')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/protected")
@requires_authentication
def protected_view(user):
    return user

