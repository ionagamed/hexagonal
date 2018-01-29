from hexagonal import auth, jsonrpc
from hexagonal.auth.helpers import minimum_access_level


@jsonrpc.bind('auth.login')
def auth_login(login, password):
    return auth.login_and_generate_token(login, password)


@jsonrpc.bind('auth.register')
@minimum_access_level('librarian')
def auth_register(login, password, role='student-patron'):
    acc = auth.register_account(login, password, role)
    return {
        'login': acc.login,
        'password': acc.password,
        'role': acc.role
    }
