from hexagonal import db


class DocumentCopy(db.Model):
    """
    Copy of a document.
    References a specific document and document type by foreign key.
    """

    __tablename__ = 'document_copies'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    document = db.relationship('Document', back_populates='copies')

    location = db.Column(db.String(200))

    loan = db.relationship('Loan', back_populates='document_copy', uselist=False)

    def __json__(self):
        loan_id = None
        if self.loan is not None:
            loan_id = self.loan.id
        return {
            'id': self.id,
            'document_id': self.document_id,
            'location': self.location,
            'loan_id': loan_id
        }
