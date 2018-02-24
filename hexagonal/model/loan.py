import datetime
import enum

from sqlalchemy.orm import aliased
from hexagonal import db, app
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from hexagonal.model.document_copy import DocumentCopy


class DocumentTransformer(Comparator):
    def operate(self, op, other, **kwargs):
        def transform(q):
            document_copy_alias = aliased(DocumentCopy)
            return q.join(document_copy_alias, Loan.document_copy).filter(op(document_copy_alias.document, other))
        return transform


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

    @hybrid_property
    def document(self):
        """
        Get the associated document.
        :return: associated document.
        """
        return self.document_copy.document

    @document.comparator
    def document(cls):
        return DocumentTransformer(cls)

    def get_overdue_fine(self):
        """
        Get total overdue fine for this loan.
        :return: the overdue fine, in rubles.
        """
        days = (datetime.date.today() - self.due_date).days
        return max(0, min(days * app.config.get('OVERDUE_FINE_PER_DAY', 100), self.document.price))

    @staticmethod
    def overdue_loan_query():
        return Loan.query.filter(Loan.status == Loan.Status.approved, Loan.due_date < datetime.date.today())

    @staticmethod
    def get_overdue_loans():
        return Loan.overdue_loan_query().all()

    @staticmethod
    def get_overdue_loan_count():
        return Loan.overdue_loan_query().count()

    @staticmethod
    def requested_loan_query():
        return Loan.query.filter(Loan.status == Loan.Status.requested)

    @staticmethod
    def get_requested_loans():
        return Loan.requested_loan_query().all()

    @staticmethod
    def get_requested_loan_count():
        return Loan.requested_loan_query().count()

    @staticmethod
    def returned_loan_query():
        return Loan.query.filter(Loan.status == Loan.Status.returned)

    @staticmethod
    def get_returned_loans():
        return Loan.requested_loan_query().all()

    @staticmethod
    def get_returned_loan_count():
        return Loan.requested_loan_query().count()

    def overdue(self):
        """ Check whether this loan is overdue. """

        return datetime.date.today() >= self.due_date

