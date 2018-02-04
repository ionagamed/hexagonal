from hexagonal import db
from hexagonal.model.helpers import model_crud_compound

document_author = db.Table(
    'document_author',
    db.Model.metadata,
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'))
)


@model_crud_compound()
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # not unique because of namesakes

    documents = db.relationship('Document', secondary=document_author, back_populates='authors')