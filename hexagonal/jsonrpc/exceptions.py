from hexagonal.jsonrpc import error_codes


class JSONRPCBaseException(Exception):
    def __init__(self, msg, error_code=error_codes.INTERNAL_ERROR, http_code=400):
        super().__init__(msg)
        self.error_code = error_code
        self.http_code = http_code
