from hexagonal import app
from hexagonal import jsonrpc
from hexagonal.auth import model


@jsonrpc.bind('auth.login')
def auth_login(login, password):
    return model.login_and_generate_token(login, password)
