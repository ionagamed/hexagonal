from hexagonal import db
from hexagonal.model.user import User


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def has_permission(self, permission):
        return True
