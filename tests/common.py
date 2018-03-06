from hexagonal import app, db
from hexagonal.model.user import User
from hexagonal.auth import register_account
import json

app.testing = True
test_client = app.test_client()


def root_login():
    return call('auth.login', ['root', 'toor'])


def get_login_pair():
    get_login_pair.cnt += 1
    return (
        'testLogin_{}'.format(get_login_pair.cnt),
        'testPassword_{}'.format(get_login_pair.cnt)
    )


get_login_pair.cnt = 0


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


def reload_db():
    db.session.commit()
    db.drop_all()
    db.create_all()

    root = User.query.filter_by(login=app.config['ROOT_LOGIN']).first()
    if root is None:
        root = register_account(
            login=app.config['ROOT_LOGIN'],
            password=app.config['ROOT_PASSWORD'],
            role=app.config['ROOT_ROLE'],

            name='Root Root',
            address='Centaurus Constellation, Alpha Star System, Third Planet',
            phone='+1 (800) I-AM-ROOT',
            card_number='-10000'
        )

    db.session.commit()
reload_db()


def create_instance(cls, **fields):
    instance = cls(**fields)
    db.session.add(instance)
    db.session.commit()
    return cls.query.filter(cls.id == instance.id).first()


def register_test_account(role, **kwargs):
    login, password = get_login_pair()
    args = {
        'login': login,
        'password': password,
        'name': login,
        'phone': '123',
        'address': '123',
        'card_number': 123,
        'role': role
    }
    args.update(kwargs)
    return register_account(**args)


