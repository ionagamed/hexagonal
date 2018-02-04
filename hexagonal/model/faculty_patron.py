from hexagonal.model.patron import Patron


class FacultyPatron(Patron):
    __mapper_args__ = {
        'polymorphic_identity': 'faculty-patron'
    }
