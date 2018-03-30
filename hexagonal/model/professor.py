from hexagonal.model.faculty_patron import FacultyPatron

from sqlalchemy.ext.hybrid import hybrid_property


class Professor(FacultyPatron):
    __mapper_args__ = {
        'polymorphic_identity': 'prof-patron'
    }

    @hybrid_property
    def queuing_priority(self):
        return 5
