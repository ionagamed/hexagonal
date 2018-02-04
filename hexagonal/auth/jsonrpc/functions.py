"""
Contains wrappers for jsonrpc to actual auth functions
"""

from hexagonal import auth, jsonrpc
from hexagonal.auth.helpers import minimum_access_level


@jsonrpc.bind('auth.login')
def auth_login(login, password):
    return auth.login_and_generate_token(login, password)


@jsonrpc.bind('auth.register')
@minimum_access_level('librarian')
def auth_register(**kwargs):
    auth.register_account(**kwargs)


@jsonrpc.bind('auth.get_my_role')
def auth_get_my_role(_token_data):
    return _token_data['role']