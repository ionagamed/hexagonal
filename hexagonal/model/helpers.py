from hexagonal.jsonrpc_crud import bind_crud
from hexagonal.auth.helpers import minimum_access_level

from hexagonal.auth import ROLE_ACCESS_LEVEL


def model_crud_compound(access_level=None):
    """
    Default compound annotation for classes.
    Uses :py:func:`hexagonal.jsonrpc_crud.bind_crud` with default settings,
    and then :py:func:`hexagonal.auth.helpers.minimum_access_level` with highest access level role
    or argument, if specified

    :param access_level: required access role. If None (default) - then use highest access level role
    :return: class wrapper
    """

    if access_level is None:
        access_level = list(ROLE_ACCESS_LEVEL.keys())[0]
        for k, v in ROLE_ACCESS_LEVEL.items():
            if v > ROLE_ACCESS_LEVEL[access_level]:
                access_level = k

    def wrapper(cls):
        return bind_crud(annotation=minimum_access_level(access_level))(cls)

    return wrapper
