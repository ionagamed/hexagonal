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


@app.after_request
def add_json_content_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response


from hexagonal.jsonrpc import route

from hexagonal.model.author import Author
from hexagonal.model.av_material import AVMaterial
from hexagonal.model.book import Book
from hexagonal.model.document import Document
from hexagonal.model.editor import Editor
from hexagonal.model.faculty_patron import FacultyPatron
from hexagonal.model.journal import Journal
from hexagonal.model.journal_article import JournalArticle
from hexagonal.model.journal_issue import JournalIssue
from hexagonal.model.keyword import Keyword
from hexagonal.model.librarian import Librarian
from hexagonal.model.patron import Patron
from hexagonal.model.publisher import Publisher
from hexagonal.model.student_patron import StudentPatron
from hexagonal.model.user import User

from hexagonal.auth.jsonrpc import functions as auth_functions
