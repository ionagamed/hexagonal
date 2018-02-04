from hexagonal.model.patron import Patron


class StudentPatron(Patron):
    __mapper_args__ = {
        'polymorphic_identity': 'student-patron'
    }
