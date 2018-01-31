from hexagonal import app

app.testing = True
test_client = app.test_client()


def call(method, params):
    return test_client.post('/api/v1/rpc', data={
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }, content_type='application/json')
