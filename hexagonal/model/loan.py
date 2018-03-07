import datetime
import enum

from sqlalchemy.ext.associationproxy import association_proxy
from hexagonal import db, app


class Loan(db.Model):
    """
    Model for one loan of a specific document by a specific user.
    Internal model, gets squashed in the api.
    """

    class Status(enum.Enum):
        approved = 1
        requested = 2
        returned = 3

    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    """ Foreign key to user. """

    user = db.relationship('User')
    """ Borrowing user id. """

    document_copy_id = db.Column(db.Integer, db.ForeignKey('document_copies.id'))
    """ Foreign key to document_copy. """

    document_copy = db.relationship('DocumentCopy', back_populates='loan')
    """ Loaned document_copy. """

    due_date = db.Column(db.Date)
    """ Date when the document_copy must be returned. """

    renewed = db.Column(db.Boolean, default=False)
    """ Whether this loan was renewed. """

    status = db.Column(db.Enum(Status), default=Status.requested)
    """ Current loan status. """

    document = association_proxy('document_copy', 'document')

    def get_overdue_fine(self):
        """
        Get total overdue fine for this loan.
        :return: the overdue fine, in rubles.
        """
        days = (datetime.date.today() - self.due_date).days
        return max(0, min(days * app.config.get('OVERDUE_FINE_PER_DAY', 100), self.document.price))

    @staticmethod
    def overdue_loan_query():
        """
        Get the query for overdue loans.

        :return: query for overdue loans.
        """

        return Loan.query.filter(Loan.status == Loan.Status.approved, Loan.due_date < datetime.date.today())

    @staticmethod
    def get_overdue_loans():
        """
        Get overdue loans.

        :return: list.
        """

        return Loan.overdue_loan_query().all()

    @staticmethod
    def get_overdue_loan_count():
        """
        Get the amount of overdue loans.

        :return: amount.
        """

        return Loan.overdue_loan_query().count()

    @staticmethod
    def requested_loan_query():
        """
        Get the query for requested loans.

        :return: query for requested loans.
        """

        return Loan.query.filter(Loan.status == Loan.Status.requested)

    @staticmethod
    def get_requested_loans():
        """
        Get requested loans.

        :return: list.
        """

        return Loan.requested_loan_query().all()

    @staticmethod
    def get_requested_loan_count():
        """
        Get the amount of requested loans.

        :return: amount.
        """

        return Loan.requested_loan_query().count()

    @staticmethod
    def returned_loan_query():
        """
        Get the query for returned loans.

        :return: query for returned loans.
        """

        return Loan.query.filter(Loan.status == Loan.Status.returned)

    @staticmethod
    def get_returned_loans():
        """
        Get returned loans.

        :return: list.
        """

        return Loan.returned_loan_query().all()

    @staticmethod
    def get_returned_loan_count():
        """
        Get the amount of returned loans.

        :return: amount.
        """

        return Loan.returned_loan_query().count()

    def overdue(self):
        """
        Check whether this loan is overdue.

        :return: whether this loan is overdue.
        """

        return datetime.date.today() >= self.due_date

    def overdue_days(self):
        """
        Gives number of overdued days of loan.

        :return: number of days
        """

        if self.overdue():
            delta = datetime.date.today() - self.due_date
            return ((delta.total_seconds()/60)/60)/24



