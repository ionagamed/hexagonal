from ..__init__ import app, db
from hashlib import sha256
from itsdangerous import JSONWebSignatureSerializer


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(40), index=True)


ALLOWED_ROLES = [
    'faculty-patron', 'student-patron', 'librarian'
]

if 'AUTH_SECRET' not in app.config:
    raise EnvironmentError('No AUTH_SECRET in config')


def encrypt_password(password):
    return sha256(password.encode('utf-8')).hexdigest()  # yeah, i know


def register_account(login, password, role):
    account = Account(
        login=login,
        password=encrypt_password(password),
        role=role
    )
    db.session.add(account)
    db.session.commit()
    return account


def login_and_generate_token(login, password):
    password = encrypt_password(password)
    account = Account.query.filter_by(login=login, password=password).first()
    if account is None:
        raise ValueError('No such account')
    else:
        s = JSONWebSignatureSerializer(app.config['AUTH_SECRET'])
        return s.dumps({
            'login': login,
            'role': account.role
        }).decode('utf-8')


def decode_token(token):
    s = JSONWebSignatureSerializer(app.config['AUTH_SECRET'])
    return s.loads(token)


try:
    Account.query.all()
except:
    db.create_all()

try:
    root = Account.query.filter_by(login=app.config['ROOT_LOGIN'])[0]
    root.password = encrypt_password(app.config['ROOT_PASSWORD'])
    root.role = app.config['ROOT_ROLE']
    db.session.commit()
except:
    register_account(
        login=app.config['ROOT_LOGIN'],
        password=app.config['ROOT_PASSWORD'],
        role=app.config['ROOT_ROLE']
    )
