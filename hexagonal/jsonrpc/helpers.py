import json


def failure(reason, code_id, request_id=None):
    if not isinstance(reason, str):
        return TypeError('reason must be string')
    if not isinstance(code_id, int):
        return TypeError('error code_id must be integer')

    dct = {
        'jsonrpc': '2.0',
        'error': {
            'code': code_id,
            'reason': reason
        }
    }

    if request_id is not None:
        dct['id'] = request_id

    return json.dumps(dct)
