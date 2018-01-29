from hexagonal import app, jsonrpc
from hexagonal.jsonrpc import helpers, error_codes
from hexagonal.jsonrpc.exceptions import JSONRPCBaseException
from flask import request
import json
import inspect


@app.route('/api/v1/rpc', methods=['POST'])
def rpc_route():
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
        return helpers.failure(
            'Please use application/json Content-Type in your requests',
            error_codes.PARSE_ERROR
        ), 400
    if 'jsonrpc' not in request.json:
        return helpers.failure(
            'jsonrpc field required in json request',
            error_codes.INVALID_REQUEST
        ), 400
    if request.json['jsonrpc'] != '2.0':
        return helpers.failure(
            'jsonrpc must be exactly "2.0"',
            error_codes.INVALID_REQUEST
        ), 400

    request_id = None
    if 'id' in request.json:
        request_id = request.json['id']
        if not isinstance(request_id, str) and not isinstance(request_id, int) and request_id is not None:
            return helpers.failure('id must be either string, integer or null', error_codes.INVALID_REQUEST), 400

    if 'method' not in request.json:
        return helpers.failure('method must be present in request', error_codes.INVALID_REQUEST, request_id), 400
    method = request.json['method']
    if not isinstance(method, str):
        return helpers.failure('method name must be string', error_codes.INVALID_REQUEST, request_id), 400

    params = None
    if 'params' in request.json:
        params = request.json['params']
        if not isinstance(params, list) and not isinstance(params, dict):
            return helpers.failure('params must be either dict or list', error_codes.INVALID_REQUEST, request_id), 400

    extension_appendix = {}

    for fn in JSONRPC_EXTENSIONS:
        try:
            r = fn()
            if r is not None:
                extension_appendix.update(r)
        except JSONRPCBaseException as e:
            return helpers.failure(str(e), e.error_code, request_id), e.http_code
        except Exception as e:
            return helpers.failure(str(e), error_codes.INTERNAL_ERROR, request_id), 400

    try:
        result = jsonrpc.call(method, params, extension_appendix)
        return json.dumps({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': result
        })
    except JSONRPCBaseException as e:
        return helpers.failure(str(e), e.error_code, request_id), e.http_code
    except Exception as e:
        return helpers.failure(str(e), error_codes.INTERNAL_ERROR, request_id), 400


JSONRPC_EXTENSIONS = []


def jsonrpc_request_extension(fn):
    """
    Register an extension to standard request parsing procedure.
    Extensions must not depend on any other extensions, as the order of application is undefined

    :param fn: extension function
    :return: same function
    """

    JSONRPC_EXTENSIONS.append(fn)
    return fn
