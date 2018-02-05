from hexagonal import db

from hexagonal.model.author import document_author

document_keyword = db.Table(
    'document_keyword',
    db.Model.metadata,
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'))
)


from hexagonal.model.keyword import Keyword


class Document(db.Model):
    """
    Base class for all documents.
    Should not be instantiated directly.
    """

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key (referenced from subclasses) """

    title = db.Column(db.String(80), unique=True, index=True, nullable=False)
    """ Document title (exists for all types) """

    price = db.Column(db.Integer, nullable=False, default=0)
    """ Document price (used in calculating overdue fine) """

    copies = db.relationship('DocumentCopy', back_populates='document')
    """ Relation with copies of this document. """

    keywords = db.relationship('Keyword', secondary=document_keyword, back_populates='documents')
    """ Relation with keywords. """

    authors = db.relationship('Author', secondary=document_author, back_populates='documents')
    """ Authors of this document. """

    type = db.Column(db.String(20), nullable=False)
    """ Polymorphic identity column for inheritance support. """

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'document'
    }
