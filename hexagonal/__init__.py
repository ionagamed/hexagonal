import os
from importlib import import_module

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


env = os.environ.get('ENV', 'docs')
config = import_module('hexagonal.config.' + env)

app = Flask('hexagonal',
            template_folder=os.path.abspath('hexagonal/ui/templates'),
            static_folder=os.path.abspath('hexagonal/ui/static'))
app.config.update(config.config)
app.secret_key = app.config['AUTH_SECRET']
app.name = app.config.get('APP_NAME', 'hexagonal')

if env == 'docs':
    SQLAlchemy.create_scoped_session = lambda x, y: None
db = SQLAlchemy(app)

from hexagonal.model.user import User
from hexagonal.model.librarian import Librarian

from hexagonal.model.av_material import AVMaterial
from hexagonal.model.book import Book
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.document import Document
from hexagonal.model.faculty_patron import FacultyPatron
from hexagonal.model.journal_article import JournalArticle
from hexagonal.model.loan import Loan
from hexagonal.model.patron import Patron
from hexagonal.model.student_patron import StudentPatron

db.create_all()

from hexagonal import test_data


import hexagonal.ui
