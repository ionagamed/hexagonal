from hexagonal.model.faculty_patron import FacultyPatron

from sqlalchemy.ext.hybrid import hybrid_property


class Instructor(FacultyPatron):
    __mapper_args__ = {
        'polymorphic_identity': 'inst-patron'
    }

    @hybrid_property
    def queuing_priority(self):
        return 2



