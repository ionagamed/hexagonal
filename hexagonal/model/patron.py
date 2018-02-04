from hexagonal.model.helpers import model_crud_compound
from hexagonal.model.user import User


@model_crud_compound()
class Patron(User):
    __mapper_args__ = {
        'polymorphic_identity': 'patron'
    }
