from hexagonal import db

from hexagonal.model.document import Document
from hexagonal.model.helpers import model_crud_compound


@model_crud_compound()
class Book(Document):
    __tablename__ = 'books'

    edition = db.Column(db.Integer, nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    publisher = db.relationship('Publisher', back_populates='books')

    __mapper_args__ = {
        'polymorphic_identity': 'book'
    }
