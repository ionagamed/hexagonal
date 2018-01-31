from hexagonal import app
import json

app.testing = True
test_client = app.test_client()


def call(method, params, token=None):
    headers = {}
    if token is not None:
        headers['Authorization'] = token
    result = json.loads(test_client.post('/api/v1/rpc', data=json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }), content_type='application/json', headers=headers).data.decode('utf-8'))
    if 'error' in result:
        raise Exception(result)
    else:
        return result['result']
