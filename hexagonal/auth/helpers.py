from hexagonal.auth import ROLE_ACCESS_LEVEL
from hexagonal.auth.jsonrpc.exceptions import JSONRPCAccessDeniedException


def minimum_access_level(level):
    if level not in ROLE_ACCESS_LEVEL:
        raise ValueError('level must be one of: ' + str(ROLE_ACCESS_LEVEL.keys()))

    def wrapper(fn):
        from functools import wraps

        @wraps(fn)
        def wrapper_impl(*args, **kwargs):
            import inspect

            current_token_data = kwargs['_token_data']
            argspec = inspect.getfullargspec(fn)
            if argspec.varkw is None and '_token_data' not in argspec.args:
                del kwargs['_token_data']
            if current_token_data is None:
                raise JSONRPCAccessDeniedException('this function requires authentication')
            if ROLE_ACCESS_LEVEL[current_token_data['role']] < ROLE_ACCESS_LEVEL[level]:
                raise JSONRPCAccessDeniedException('required at least ' + level + ' access level')
            return fn(*args, **kwargs)

        return wrapper_impl

    return wrapper
