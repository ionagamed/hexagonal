from hexagonal.model.user import User
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.book import Book
from hexagonal.model.loan import Loan
from hexagonal.auth.permissions import Permission
import datetime
from hexagonal import db

from sqlalchemy.ext.hybrid import hybrid_property


class Patron(User):
    """
    Abstract base class for patrons.
    Should not be directly instantiated
    """

    __mapper_args__ = {
        'polymorphic_identity': 'patron'
    }

    permissions = [Permission.checkout]

    def get_checkout_period_for(self, document):
        """
        Get checkout period for a specific document.
        Abstract in User.

        :param document: to be checked out
        :return: timedelta
        """
        raise NotImplementedError()

    def overdue_loan_query(self):
        """
        Get BaseQuery for all overdue loans of this user.

        :return: BaseQuery
        """
        return Loan.overdue_loan_query().filter(Loan.user == self)

    def get_overdue_loans(self):
        """
        Get current overdue associated loans.

        :return: list of loans
        """

        return self.overdue_loan_query().all()

    def get_overdue_loan_count(self):
        """
        Get the amount of overdue associated items.

        :return: amount
        """
        return self.overdue_loan_query().count()

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

        if isinstance(document_copy.document, Book) and document_copy.document.reference:
            raise ValueError(
                'document {} (id {}) is a reference book'.format(document_copy.document.title, document_copy.id))

        document_copy.loan = Loan(user_id=self.id, document_copy_id=document_copy.id)
        document_copy.loan.due_date = datetime.date.today() + self.get_checkout_period_for(document_copy.document)
        db.session.add(document_copy)
        db.session.add(document_copy.loan)
        db.session.commit()

        return document_copy.loan

    def loan_query(self):
        """
        Get BaseQuery for all approved loans with borrowed documents

        :return: BaseQuery
        """

        return Loan.query.filter(Loan.user_id == self.id, Loan.status == Loan.Status.approved)

    def get_loans(self):
        """
        Get all approved loans for this patron.

        :return: list.
        """
        return self.loan_query().all()

    def get_loan_count(self):
        """
        Get the amount of all approved loans for this patron.

        :return: list.
        """
        return self.loan_query().count()

    def get_borrowed_document_copies(self):
        """
        Get document copies that are currently borrowed by this user.

        :return: list of document_copies
        """

        return list(map(
            lambda x: x.document_copy,
            self.loan_query().all()
        ))

    def get_borrowed_document_copy_count(self):
        """
        Get the amount of borrowed document copies.

        :return: amount
        """

        return self.loan_query().count()

    def requested_loans_query(self):
        return Loan.query.filter(Loan.user_id == self.id, Loan.status == Loan.Status.requested)

    def get_requested_loans(self):
        return self.requested_loans_query().all()

    def get_requested_loan_count(self):
        return self.requested_loans_query().count()

    def returned_loans_query(self):
        return Loan.query.filter(Loan.user_id == self.id, Loan.status == Loan.Status.returned)

    def get_returned_loans(self):
        return self.returned_loans_query().all()

    def get_returned_loan_count(self):
        return self.returned_loans_query().count()

    @hybrid_property
    def queuing_priority(self):
        raise NotImplementedError
