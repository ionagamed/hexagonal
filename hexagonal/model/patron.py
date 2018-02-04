from hexagonal.model.user import User


class Patron(User):
    __mapper_args__ = {
        'polymorphic_identity': 'patron'
    }
