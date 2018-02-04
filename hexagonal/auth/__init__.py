from hexagonal import app, db, env
from hashlib import sha256
from itsdangerous import TimedJSONWebSignatureSerializer
from hexagonal.auth.jsonrpc import extensions
from hexagonal.jsonrpc_crud import bind_crud


@bind_crud()
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(40), index=True)


ROLE_ACCESS_LEVEL = {
    'student-patron': 1,
    'faculty-patron': 2,
    'librarian':      3
}

if 'AUTH_SECRET' not in app.config:
    raise EnvironmentError('No AUTH_SECRET in config')

token_max_age = app.config.get('AUTH_MAX_TOKEN_AGE', 60 * 60 * 5)  # 5 hrs


def encrypt_password(password):
    """
    Encrypt the password for storage in database

    :param password: to be encrypted
    :return: the encrypted password
    """
    return sha256(password.encode('utf-8')).hexdigest()  # yeah, i know


def register_account(login, password, role):
    """
    Register a new account

    :param login: login of the new account
    :param password: password of the new account
    :param role: role of the new account
    :return: instance of the created :py:class:`Account`
    """
    account = Account(
        login=login,
        password=encrypt_password(password),
        role=role
    )
    db.session.add(account)
    db.session.commit()
    return account


def login_and_generate_token(login, password):
    """
    Try to login the user with specified credentials.
    If no such user exists (either not valid login, or not valid password) raises ValueError.

    :param login: login of trying user
    :param password: password of trying user
    :return: new generated token (see :py:func:`decode_token`)
    """
    password = encrypt_password(password)
    account = Account.query.filter_by(login=login, password=password).first()
    if account is None:
        raise ValueError('No such account')
    else:
        s = TimedJSONWebSignatureSerializer(app.config['AUTH_SECRET'], expires_in=token_max_age)
        return s.dumps({
            'login': login,
            'role': account.role
        }).decode('utf-8')


def decode_token(token):
    """
    Try to decode token, which was (or wasn't) received from the user.
    Throws an exception upon failure (invalid token for any reason).

    :param token: to be decoded
    :return: token data, which was embedded there
    """
    s = TimedJSONWebSignatureSerializer(app.config['AUTH_SECRET'], expires_in=token_max_age)
    return s.loads(token)


if env != 'docs':
    try:
        Account.query.all()
    except:
        db.session.commit()
        db.create_all()


    root = Account.query.filter_by(login=app.config['ROOT_LOGIN']).first()
    if root is None:
        root = register_account(
            login=app.config['ROOT_LOGIN'],
            password=app.config['ROOT_PASSWORD'],
            role=app.config['ROOT_ROLE']
        )

    db.session.commit()

