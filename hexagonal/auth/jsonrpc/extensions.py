from hexagonal.jsonrpc.route import jsonrpc_request_extension
from hexagonal import auth
from flask import request


@jsonrpc_request_extension
def pull_token_data():
    if 'Authorization' in request.headers:
        current_token_data = auth.decode_token(request.headers['Authorization'])

        if 'login' not in current_token_data:
            raise ValueError('login not in token')

        if 'role' not in current_token_data:
            raise ValueError('role not in token')

        return {
            '_token_data': current_token_data
        }
