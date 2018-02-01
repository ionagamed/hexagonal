import os
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hexagonal.jsonrpc import helpers, error_codes

env = os.environ.get('ENV', 'docs')
config = import_module('hexagonal.config.' + env)

app = Flask('hexagonal')
app.config.update(config.config)
app.name = app.config.get('APP_NAME', 'hexagonal')

if env == 'docs':
    SQLAlchemy.create_scoped_session = lambda x, y: None
db = SQLAlchemy(app)

from hexagonal.jsonrpc import route
from hexagonal.auth.jsonrpc import functions as auth_functions
