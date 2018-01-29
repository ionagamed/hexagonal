from hexagonal.jsonrpc.exceptions import JSONRPCBaseException
from hexagonal.jsonrpc import error_codes


class JSONRPCAccessDeniedException(JSONRPCBaseException):
    def __init__(self, msg):
        super().__init__(msg, error_codes.AUTH__ACCESS_DENIED, 403)
