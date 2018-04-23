from hexagonal import db
from hexagonal.auth.permissions import Permission
from hexagonal.model.user import User


class Librarian(User):
    """
    Librarian type of user.
    """

    __tablename__ = 'librarians'

    __mapper_args__ = {
        'polymorphic_identity': 'librarian'
    }

    access_level = db.Column(db.Integer, default=1, nullable=False)

    def has_permission(self, permission):
        """
        Whether this user has the required permission.

        :param permission: permission to be checked.
        :return: whether the current user has the required permission.
        """

        if self.access_level <= 0 or self.access_level >= 4:
            raise ValueError('Librarian has wrong access level')

        permission_map = [
            [],
            [
                Permission.manage,
                Permission.modify_document,
                Permission.modify_patron
            ],
            [
                Permission.manage,
                Permission.modify_document,
                Permission.modify_patron,
                Permission.create_document,
                Permission.create_patron,
                Permission.outstanding_request
            ],
            [
                Permission.manage,
                Permission.modify_document,
                Permission.modify_patron,
                Permission.create_document,
                Permission.create_patron,
                Permission.delete_document,
                Permission.delete_patron,
                Permission.outstanding_request
            ]
        ]

        return permission in permission_map[self.access_level]
