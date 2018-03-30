from hexagonal.model.faculty_patron import FacultyPatron

from sqlalchemy.ext.hybrid import hybrid_property


class TeachingAssistant(FacultyPatron):
    __mapper_args__ = {
        'polymorphic_identity': 'ta-patron'
    }

    @hybrid_property
    def queuing_priority(self):
        return 3
