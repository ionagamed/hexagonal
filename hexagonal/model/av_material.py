from hexagonal.model.document import Document
from hexagonal import db


class AVMaterial(Document):
    """
    AVMaterial document type.
    These could be checked out for 2 weeks by anyone.
    """

    __tablename__ = 'av_materials'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Primary foreign key to documents. """

    __mapper_args__ = {
        'polymorphic_identity': 'av_material'
    }
