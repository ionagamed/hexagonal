from hexagonal.model.helpers import model_crud_compound
from hexagonal.model.patron import Patron


@model_crud_compound()
class FacultyPatron(Patron):
    __mapper_args__ = {
        'polymorphic_identity': 'faculty-patron'
    }
