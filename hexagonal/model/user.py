import datetime

from hexagonal import db
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.loan import Loan


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), index=True, nullable=False)

    name = db.Column(db.String(80), index=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    card_number = db.Column(db.String(80), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    def get_checkout_period_for(self, document):
        raise NotImplementedError()

    def get_overdue_loans(self):
        raise NotImplementedError()

    def get_total_overdue_fine(self):
        raise NotImplementedError()

    def checkout(self, document_copy):
        if not isinstance(document_copy, DocumentCopy):
            raise TypeError('document_copy should be of type DocumentCopy')

        if document_copy.loan is not None:
            raise ValueError('document {} (id {}) is already loaned by user {} (id {})'.format(
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
