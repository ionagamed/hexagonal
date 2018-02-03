import json


def failure(reason, code, request_id=None):
    """
    Failure helper, to construct an error with a specified reason.

    :param reason: reason of failure
    :param code: error code
    :param request_id: [optional] request_id to be sent to client
    :return: json string with response body
    """

    if not isinstance(reason, str):
        return TypeError('reason must be string')
    if not isinstance(code, int):
        return TypeError('error code_id must be integer')

    dct = {
        'jsonrpc': '2.0',
        'error': {
            'code': code,
            'reason': reason
        }
    }

    if request_id is not None:
        dct['id'] = request_id

    return json.dumps(dct)
