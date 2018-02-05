import datetime

from hexagonal import db
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.loan import Loan


class User(db.Model):
    """
    Base class for all users in the system.
    Should not be directly instantiated. (`hexagonal.auth` currently does that, but i'm working on it)
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    login = db.Column(db.String(80), unique=True, index=True, nullable=False)
    """ Login of the user. Must be unique. """

    password = db.Column(db.String(128), nullable=False)
    """ Password hash of the user. """

    role = db.Column(db.String(20), index=True, nullable=False)
    """ Polymorphic identity of the user. Used to implement inheritance. """

    name = db.Column(db.String(80), index=True, nullable=False)
    """ User's full name. """

    address = db.Column(db.String(80), nullable=False)
    """ User's full address. """

    phone = db.Column(db.String(80), nullable=False)
    """ User's phone number. """

    card_number = db.Column(db.String(80), nullable=False)
    """ User's library card number. """

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    def get_checkout_period_for(self, document):
        """
        Get checkout period for a specific document.
        Abstract in User.

        :param document: to be checked out
        :return: timedelta
        """
        raise NotImplementedError()

    def get_overdue_loans(self):
        """
        Get current overdue associated loans.
        Abstract in User.

        :return: list of loans
        """
        raise NotImplementedError()

    def get_total_overdue_fine(self):
        """
        Get total current overdue fine across all loans.
        Abstract in User.

        :return: total overdue fine, in rubles
        """
        raise NotImplementedError()

    def checkout(self, document_copy):
        """
        Try to checkout the required document_copy.
        Raises TypeError if document_copy is not a DocumentCopy.
        Raises ValueError if document_copy is not available for loan.

        :param document_copy: to be checked out.
        :return: loan object
        """

        if not isinstance(document_copy, DocumentCopy):
            raise TypeError('document_copy should be of type DocumentCopy')

        if document_copy.loan is not None:
            raise ValueError('document {} (id {}) is already borrowed by user {} (id {})'.format(
                document_copy.document.title,
                document_copy.id,
                document_copy.loan.user.name,
                document_copy.loan.user.id
            ))

        document_copy.loan = Loan(user_id=self.id, document_copy_id=document_copy.id)
        document_copy.loan.due_date = datetime.date.today() + self.get_checkout_period_for(document_copy.document)
        db.session.add(document_copy)
        db.session.add(document_copy.loan)
        db.session.commit()

        return document_copy.loan

    def get_borrowed_document_copies(self):
        """
        Get document copies that are currently borrowed by this user.

        :return: list of document_copies
        """

        return list(map(
            lambda x: x.document_copy,
            Loan.query.filter(Loan.user_id == self.id)
        ))
