from hexagonal.jsonrpc.helpers import failure
import inspect

RPC_BINDINGS = {}


def bind(name=None):
    """
    Bind the function handler under a specific name to be available to calls.
    Intended to use as a decorator.

    :param name: [optional] function name. if not specified, uses function's original name
    :return: function wrapper
    """

    def wrapper(handler):
        name_ = name
        if name_ is None:
            name_ = handler.__name__
        RPC_BINDINGS[name_] = handler
        return handler

    return wrapper


def call(name, args=None, optional=None):
    """
    Perform the actual call of a function by name and args object.

    `args` can be None - then function is called without arguments.
    `args` can be a list - then function is called with positional arguments.
    `args` can be a dict - then function is called with named arguments.

    `optional` is a dict with named arguments which are passed to a function, if present in the declaration.

    :param name: function name
    :param args: arguments of the function
    :param optional: optional arguments of the function
    :return: result of function call
    """

    if name not in RPC_BINDINGS:
        raise ValueError('no such function')
    if optional is not None and not isinstance(optional, dict):
        raise TypeError('optionals must be dict')

    func = RPC_BINDINGS[name]

    kwargs = {}
    argspec = inspect.getfullargspec(func)
    for k, v in optional.items():
        if k in argspec.kwonlyargs or k in argspec.args or argspec.varkw:
            kwargs[k] = v

    if args is None:
        return func(**kwargs)
    if isinstance(args, list):
        return func(*args, **kwargs)
    if isinstance(args, dict):
        args.update(kwargs)
        return func(**args)

    raise TypeError('args is not None, list or dict')
