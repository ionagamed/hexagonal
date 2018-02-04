import datetime

from hexagonal.model.book import Book
from hexagonal.model.document import Document
from hexagonal.model.patron import Patron


class StudentPatron(Patron):
    __mapper_args__ = {
        'polymorphic_identity': 'student-patron'
    }

    def get_checkout_period_for(self, document):
        if not isinstance(document, Document):
            raise TypeError('document should be of type Document')

        if isinstance(document, Book):
            if document.bestseller:
                return datetime.timedelta(weeks=2)
            else:
                return datetime.timedelta(weeks=3)
        return datetime.timedelta(weeks=2)
