from hexagonal import db

from hexagonal.model.document import Document
from hexagonal.model.helpers import ids


class Book(Document):
    """
    Book document type.
    """

    __tablename__ = 'books'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Integer primary foreign key to documents. """

    edition = db.Column(db.Integer)
    """ Book edition. """

    bestseller = db.Column(db.Boolean, default=False)
    """ Whether this book is a bestseller. """

    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    """ Foreign key to publisher. """

    publisher = db.relationship('Publisher', back_populates='books')
    """ Relation with publisher. """

    __mapper_args__ = {
        'polymorphic_identity': 'book'
    }

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'copy_ids': ids(self.copies),
            'keywords': map(lambda x: x.name, self.keywords),
            'authors': map(lambda x: x.name, self.authors),
            'edition': self.edition,
            'bestseller': self.bestseller,
            'publisher': self.publisher.name
        }
