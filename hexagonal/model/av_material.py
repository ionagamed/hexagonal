from hexagonal.model.document import Document


class AVMaterial(Document):
    __tablename__ = 'av_materials'

    __mapper_args__ = {
        'polymorphic_identity': 'av_material'
    }