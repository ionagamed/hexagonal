import os
from importlib import import_module

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, get_debug_queries


env = os.environ.get('ENV', 'docs')
config = import_module('hexagonal.config.' + env)

app = Flask('hexagonal',
            template_folder=os.path.abspath('hexagonal/ui/templates'),
            static_folder=os.path.abspath('hexagonal/ui/static'))
app.debug = True
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
from hexagonal.model.visiting_professor_patron import VisitingProfessorPatron

if env != 'docs':
    db.create_all()
    from hexagonal.auth import create_root
    create_root()

if env != 'testing' and env != 'docs':
    from hexagonal import test_data


import hexagonal.ui


def overdue_loan_count_wrapper():
    return Loan.get_overdue_loan_count()


def requested_loan_count_wrapper():
    return Loan.get_requested_loan_count()


def returned_loan_count_wrapper():
    return Loan.get_returned_loan_count()


def random_wrapper():
    import random
    return random.randint(0, 100500)

app.jinja_env.globals['get_all_overdue_loan_count'] = overdue_loan_count_wrapper
app.jinja_env.globals['get_all_requested_loan_count'] = requested_loan_count_wrapper
app.jinja_env.globals['get_all_returned_loan_count'] = returned_loan_count_wrapper
app.jinja_env.globals['Loan'] = Loan
app.jinja_env.globals['rnd'] = random_wrapper

if 'JINJA_GLOBALS' in app.config:
    app.jinja_env.globals.update(app.config['JINJA_GLOBALS'])
