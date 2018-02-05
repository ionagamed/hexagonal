from hexagonal import db

from hexagonal.model.document import document_keyword


class Keyword(db.Model):
    """
    Keyword model for documents.
    Used for quick search for keywords and related documents.
    Internal model, gets squashed in the api.
    """

    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    documents = db.relationship('Document', secondary=document_keyword, back_populates='keywords')
