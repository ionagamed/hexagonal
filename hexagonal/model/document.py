from sqlalchemy.ext.associationproxy import association_proxy

from hexagonal import db
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.searchable import Searchable
from sqlalchemy.ext.hybrid import hybrid_property


class Document(db.Model, Searchable):
    """
    Base class for all documents.
    Should not be instantiated directly.

    Contains common fields for all documents, and inherits from :py:class:`hexagonal.model.searchable.Searchable`,
    adding search capability.

    Fuzzy search fields are `title` and `type`.
    Fuzzy array search fields are `keywords` and `authors`.
    """

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key (referenced from subclasses) """

    title = db.Column(db.String(80), unique=True, index=True, nullable=False)
    """ Document title (exists for all types) """

    price = db.Column(db.Integer, nullable=False, default=0)
    """ Document price (used in calculating overdue fine) """

    copies = db.relationship('DocumentCopy', back_populates='document', cascade='all, delete-orphan')
    """ Relation with copies of this document. """

    keywords = db.Column(db.ARRAY(db.String(80)))
    """ Relation with keywords. """

    authors = db.Column(db.ARRAY(db.String(80)))
    """ Authors of this document. """

    type = db.Column(db.String(20), nullable=False)
    """ Polymorphic identity column for inheritance support. """

    queued_requests = db.relationship('QueuedRequest', back_populates='document')
    awaiting_patrons = association_proxy('queued_requests', 'patron')

    outstanding = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'document'
    }

    fuzzy_search_fields = ['title', 'type']
    fuzzy_array_search_fields = ['keywords', 'authors']

    @hybrid_property
    def available_copies(self):
        """
        Hybrid property for currently available copies of this document.
        Available copies are copies which don't have an associated loan.
        """

        return DocumentCopy.query.filter(
            DocumentCopy.document == self, DocumentCopy.loan == None
        ).all()

    def outstanding_request(self):
        self.outstanding = True
        db.session.add(self)
        for qr in self.queued_requests:
            db.session.delete(qr)
        db.session.commit()
