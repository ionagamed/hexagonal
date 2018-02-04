from hexagonal import db

from hexagonal.model.user import User


class Librarian(User):
    __mapper_args__ = {
        'polymorphic_identity': 'librarian'
    }