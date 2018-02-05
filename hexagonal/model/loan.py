import datetime

from hexagonal import db, app


class Loan(db.Model):
    """
    Model for one loan of a specific document by a specific user.
    Internal model, gets squashed in the api.
    """

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

    def get_document(self):
        """
        Get the associated document.
        :return: associated document.
        """
        return self.document_copy.document

    def get_overdue_fine(self):
        """
        Get total overdue fine for this loan.
        :return: the overdue fine, in rubles.
        """
        days = (datetime.date.today() - self.due_date).days
        return max(0, min(days * app.config.get('OVERDUE_FINE_PER_DAY', 100), self.get_document().price))
