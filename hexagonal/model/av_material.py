from hexagonal.model.document import Document
from hexagonal import db
from hexagonal.model.helpers import ids


class AVMaterial(Document):
    """
    AVMaterial document type.
    """

    __tablename__ = 'av_materials'

    id = db.Column(db.Integer, db.ForeignKey('documents.id'), primary_key=True)
    """ Primary foreign key to documents. """

    __mapper_args__ = {
        'polymorphic_identity': 'av_material'
    }

    def __json__(self):
        """
        JSON representation for a given instance.
        :return: JSON-serializable representation of self.
        """
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'copy_ids': ids(self.copies),
            'keywords': map(lambda x: x.name, self.keywords),
            'authors': map(lambda x: x.name, self.authors)
        }
