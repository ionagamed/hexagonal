from hexagonal import app
from hexagonal import jsonrpc


@jsonrpc.bind('auth.login')
def auth_login(s):
    return s
