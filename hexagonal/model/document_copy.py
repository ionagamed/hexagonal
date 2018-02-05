from hexagonal import db


class DocumentCopy(db.Model):
    """
    Copy of a document.
    References a specific document and document type by foreign key.
    """

    __tablename__ = 'document_copies'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    """ Foreign key to documents. """
    document = db.relationship('Document', back_populates='copies')
    """ Associated document. """

    location = db.Column(db.String(200))
    """ Location of the copy in the physical library. """

    loan = db.relationship('Loan', back_populates='document_copy', uselist=False)
    """ Relation to current loan. May be None when document is available. """

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        loan_id = None
        if self.loan is not None:
            loan_id = self.loan.id
        return {
            'id': self.id,
            'document_id': self.document_id,
            'location': self.location,
            'loan_id': loan_id
        }
