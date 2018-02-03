from hexagonal.jsonrpc import error_codes


class JSONRPCBaseException(Exception):
    """
    Base exception for any thrown jsonrpc exception.
    """
    def __init__(self, msg, error_code=error_codes.INTERNAL_ERROR, http_code=400):
        super().__init__(msg)

        self.error_code = error_code
        """
        Error code, which is sent in body of response.
        """

        self.http_code = http_code
        """
        HTTP code, which is sent over http.
        """
