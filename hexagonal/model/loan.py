import datetime

from hexagonal import db, app


class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    document_copy_id = db.Column(db.Integer, db.ForeignKey('document_copies.id'))
    document_copy = db.relationship('DocumentCopy', back_populates='loan')

    due_date = db.Column(db.Date)
    renewed = db.Column(db.Boolean, default=False)

    def get_document(self):
        return self.document_copy.document

    def get_overdue_fine(self):
        days = (datetime.date.today() - self.due_date).days
        return min(days * app.config.get('OVERDUE_FINE_PER_DAY', 100), self.get_document().price)
