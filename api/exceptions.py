class GApiError(Exception):
    pass


class GApiUnavailable(GApiError):
    pass


class GApiForbidden(GApiError):
    pass


class GApiNotFound(GApiError):
    pass


class GApiBadRequest(GApiError):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
