import datetime

from hexagonal.model.book import Book
from hexagonal.model.document import Document
from hexagonal.model.patron import Patron
from hexagonal.model.user import User


class StudentPatron(Patron):
    """
    Student patron user type.
    Internal model, gets squashed in the api.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'student-patron'
    }

    def get_checkout_period_for(self, document):
        """
        Get checkout period for a specific document.
        Abstract in User.

        :param document: to be checked out
        :return: timedelta
        """

        if not isinstance(document, Document):
            raise TypeError('document should be of type Document')

        if isinstance(document, Book):
            if document.reference:
                raise ValueError('type is not available to check out')
            if document.bestseller:
                return datetime.timedelta(weeks=2)
            else:
                return datetime.timedelta(weeks=3)
        return datetime.timedelta(weeks=2)
