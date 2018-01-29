from hexagonal.jsonrpc.helpers import failure

RPC_BINDINGS = {}


def bind(name=None):
    """
    Bind the function handler under a specific name to be available to calls
    Intended to use as a decorator

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


def call(name, args=None):
    """
    Perform the actual call of a function by name and args object

    args can be None - then function is called without arguments
    args can be a list - then function is called with positional arguments
    args can be a dict - then function is called with named arguments

    :param name: function name
    :param args: arguments of the function
    :return: result of function call
    """

    if name not in RPC_BINDINGS:
        raise ValueError('no such function')
    func = RPC_BINDINGS[name]
    if args is None:
        return func()
    if isinstance(args, list):
        return func(*args)
    if isinstance(args, dict):
        return func(**args)

    raise TypeError('args is not None, list or dict')
