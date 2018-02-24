from hexagonal import db

from hexagonal.model.document import Document


class Book(Document):
    """
    Book document type.
    """

    __tablename__ = 'books'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Integer primary foreign key to documents. """

    edition = db.Column(db.Integer)
    """ Book edition. """

    publishment_year = db.Column(db.Integer)
    """ Publishment year. """

    bestseller = db.Column(db.Boolean, default=False)
    """ Whether this book is a bestseller. """

    publisher = db.Column(db.String(80))
    """ Relation with publisher. """

    reference = db.Column(db.Boolean, default=False)
    """ Whether this book is a reference book"""

    __mapper_args__ = {
        'polymorphic_identity': 'book'
    }
