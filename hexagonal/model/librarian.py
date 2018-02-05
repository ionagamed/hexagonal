from hexagonal.model.user import User


class Librarian(User):
    """
    Librarian type of user.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'librarian'
    }
