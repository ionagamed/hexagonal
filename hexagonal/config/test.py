import os

config = {
    'APP_NAME': 'hexagonal-test',
    'AUTH_SECRET': 'secret',

    'ROOT_LOGIN': 'root',
    'ROOT_PASSWORD': 'toor',
    'ROOT_ROLE': 'librarian'
}

postgres_password = os.environ.get('PGPASSWORD', 'test')
config['SQLALCHEMY_DATABASE_URI'] = 'postgressql://postgres:{}@127.0.0.1/postgres'.format(postgres_password)
