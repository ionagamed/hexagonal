import os

config = {
    'APP_NAME': 'hexagonal-dev',
    'AUTH_SECRET': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'ROOT_LOGIN': 'root',
    'ROOT_PASSWORD': 'toor',
    'ROOT_ROLE': 'admin',

    'UI_ROOT': '/',
    'TEMPLATES_AUTO_RELOAD': True,

    'JINJA_GLOBALS': {
        'loan_color': {
            'Status.overdue': 'red',
            'Status.requested': 'teal',
        },
        'product_version': '0.0.2'
    }
}

postgres_password = os.environ.get('PGPASSWORD', 'test')
config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@db/postgres'.format(postgres_password)
