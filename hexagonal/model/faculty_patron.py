import datetime

from hexagonal.model.book import Book
from hexagonal.model.document import Document
from hexagonal.model.patron import Patron


class FacultyPatron(Patron):
    """
    Faculty patron user type.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'faculty-patron'
    }

    def get_checkout_period_for(self, document):
        if not isinstance(document, Document):
            raise TypeError('document should be of type Document')

        if isinstance(document, Book):
            return datetime.timedelta(weeks=4)
        return datetime.timedelta(weeks=2)
