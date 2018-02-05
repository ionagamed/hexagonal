from hexagonal.model.user import User


class Patron(User):
    """
    Abstract base class for patrons.
    Should not be directly instantiated
    """

    __mapper_args__ = {
        'polymorphic_identity': 'patron'
    }
