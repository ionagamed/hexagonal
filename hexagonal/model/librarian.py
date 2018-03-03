from hexagonal.model.user import User


class Librarian(User):
    """
    Librarian type of user.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'librarian'
    }

    def has_permission(self, permission):
        """
        Whether this user has the required permission.
        Librarian has all permissions.

        :param permission: permission to be checked.
        :return: whether the current user has the required permission.
        """

        return True
