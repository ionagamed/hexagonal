from hexagonal import app
from hexagonal import jsonrpc

@jsonrpc.bind
def auth_login(s):
    return s
