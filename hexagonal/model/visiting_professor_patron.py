import datetime

from hexagonal.model.document import Document
from hexagonal.model.patron import Patron


class VisitingProfessorPatron(Patron):
    """
    Visiting Professor patron user type.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'vp-patron'
    }

    def get_checkout_period_for(self, document):
        """
        Get checkout period for a specific document.

        :param document: to be checked out
        :return: timedelta
        """

        if not isinstance(document, Document):
            raise TypeError('document should be of type Document')
        else:
            if document.reference:
                raise ValueError('type is not available to check out')
            return datetime.timedelta(weeks=1)
