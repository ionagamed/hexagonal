import datetime

from hexagonal import db
from hexagonal.model.document_copy import DocumentCopy
from hexagonal.model.loan import Loan
from hexagonal.model.searchable import Searchable


class User(db.Model, Searchable):
    """
    Base class for all users in the system.
    Should not be directly instantiated. (`hexagonal.auth` currently does that, but i'm working on it)
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    """ Integer primary key. """

    login = db.Column(db.String(80), unique=True, index=True, nullable=False)
    """ Login of the user. Must be unique. """

    password = db.Column(db.String(128), nullable=False)
    """ Password hash of the user. """

    reset_password = db.Column(db.Boolean, default=False)
    """ Reset password flag. If true, on next login user would be prompted to reset the password. """

    role = db.Column(db.String(20), index=True, nullable=False)
    """ Polymorphic identity of the user. Used to implement inheritance. """

    name = db.Column(db.String(80), index=True, nullable=False)
    """ User's full name. """

    address = db.Column(db.String(80), nullable=False)
    """ User's full address. """

    phone = db.Column(db.String(80), nullable=False)
    """ User's phone number. """

    card_number = db.Column(db.String(80), nullable=False)
    """ User's library card number. """

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    permissions = []

    fuzzy_search_fields = ['name', 'address', 'phone']

    def has_permission(self, permission):
        """
        Whether this user has the required permission.

        By default returns whether permission is present in the class static field `permissions`.

        :param permission: permission to be checked.
        :return: whether the current user has the required permission.
        """

        return permission in self.permissions
