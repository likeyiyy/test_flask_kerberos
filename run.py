from flask import Flask
from flask_kerberos import init_kerberos, _gssapi_authenticate, _forbidden, _unauthorized
from flask import Response
from flask import _request_ctx_stack as stack
from flask import make_response
from flask import request
from functools import wraps
from socket import gethostname
from os import environ
import kerberos


app = Flask(__name__)
init_kerberos(app, hostname='webserver.example.com')


@app.route('/')
def hello_world():
    return 'Hello, World!'



def requires_authentication(function):
    '''
    Require that the wrapped view function only be called by users
    authenticated with Kerberos. The view function will have the authenticated
    users principal passed to it as its first argument.

    :param function: flask view function
    :type function: function
    :returns: decorated function
    :rtype: function
    '''
    @wraps(function)
    def decorated(*args, **kwargs):
        header = request.headers.get("Authorization")
        if header:
            ctx = stack.top
            token = ''.join(header.split()[1:])
            rc = _gssapi_authenticate(token)
            if rc == kerberos.AUTH_GSS_COMPLETE:
                response = function(ctx.kerberos_user, *args, **kwargs)
                response = make_response(response)
                if ctx.kerberos_token is not None:
                    response.headers['WWW-Authenticate'] = ' '.join(['negotiate',
                                                                     ctx.kerberos_token])
                return response
            elif rc != kerberos.AUTH_GSS_CONTINUE:
                return _forbidden()
        return _unauthorized()
    return decorated


@app.route("/protected")
@requires_authentication
def protected_view(user):
    return user

