from hexagonal.model.document import Document
from hexagonal.model.helpers import model_crud_compound


@model_crud_compound()
class AVMaterial(Document):
    __tablename__ = 'av_materials'

    __mapper_args__ = {
        'polymorphic_identity': 'av_material'
    }