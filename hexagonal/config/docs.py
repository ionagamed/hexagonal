import os

config = {
    'APP_NAME': 'hexagonal-test',
    'AUTH_SECRET': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'ROOT_LOGIN': 'root',
    'ROOT_PASSWORD': 'toor',
    'ROOT_ROLE': 'librarian'
}

postgres_password = os.environ.get('PGPASSWORD', 'test')
config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost/postgres'.format(postgres_password)
