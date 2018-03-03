from hexagonal import app, db
from hashlib import sha256
from itsdangerous import TimedJSONWebSignatureSerializer
from hexagonal.model.user import User


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


def change_password(login_or_id, new_password):
    """
    Change the password of the existing user

    :param login_or_id: login or id of an existing user
    :param new_password: new password for the user
    :return: None
    """

    password = encrypt_password(new_password)
    if isinstance(login_or_id, str):
        user = User.query.filter(User.login == login_or_id).first()
    else:
        user = User.query.filter(User.id == login_or_id).first()
    user.password = password
    db.session.add(user)
    db.session.commit()


def register_account(**kwargs):
    """
    Register a new account

    :param kwargs: field of the new account
    :return: instance of the created :py:class:`Account`
    """

    if '_token_data' in kwargs:
        del kwargs['_token_data']
    kwargs['password'] = encrypt_password(kwargs['password'])
    if isinstance(kwargs['role'], str):
        account = User(**kwargs)
    else:
        cls = kwargs['role']
        del kwargs['role']
        account = cls(**kwargs)
    db.session.add(account)
    db.session.commit()
    return User.query.filter(User.id == account.id).first()


def login_and_generate_token(login, password):
    """
    Try to login the user with specified credentials.
    If no such user exists (either not valid login, or not valid password) raises ValueError.

    :param login: login of trying user
    :param password: password of trying user
    :return: new generated token (see :py:func:`decode_token`)
    """

    password = encrypt_password(password)
    account = User.query.filter_by(login=login, password=password).first()
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


def create_root():
    """
    Create a default root user, if not exists
    """

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

