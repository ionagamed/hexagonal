import enum
from hexagonal import User


class Permission(enum.Enum):
    """
    Permission enum.
    Users can have any subset of these, and routes are managed by these.
    See :py:func:`hexagonal.auth.permissions.required_permission`
    """

    checkout = 'checkout'
    manage = 'manage'


def required_permission(permission):
    """
    Required permission route decorator.
    Must not be used without a route.

    :param permission: required permission
    :return decorated route function
    """

    if not isinstance(permission, Permission):
        raise ValueError('{} is not a valid permission', str(permission))

    from functools import wraps
    import flask

    def redirect():
        try:
            return flask.redirect(required_permission.redirect_address)
        except:
            return flask.Response(status=404)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if 'login' not in flask.session:
                return redirect()
            user = User.query.filter(User.login == flask.session['login']).first()
            if user.has_permission(permission):
                return fn(*args, **kwargs)
            else:
                return redirect()
        return wrapper

    return decorator
required_permission.redirect_address = '/login'
