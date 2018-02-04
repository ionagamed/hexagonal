from hexagonal import db

from hexagonal.model.document import Document
from hexagonal.model.helpers import ids


class Book(Document):
    __tablename__ = 'books'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    edition = db.Column(db.Integer)
    bestseller = db.Column(db.Boolean, default=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    publisher = db.relationship('Publisher', back_populates='books')

    __mapper_args__ = {
        'polymorphic_identity': 'book'
    }

    def __json__(self):
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
