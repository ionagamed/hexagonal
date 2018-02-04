from hexagonal import db

from hexagonal.model.document import document_keyword
from hexagonal.model.helpers import model_crud_compound


@model_crud_compound()
class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    documents = db.relationship('Document', secondary=document_keyword, back_populates='keywords')
