from fastapi import status


class DomainError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "domain_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def to_dict(self):
        return {"error": self.code, "message": self.message}


class NotFoundError(DomainError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class PermissionDenied(DomainError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden"


class AuthenticationError(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"


class ValidationError(DomainError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"


ERROR_CLASSES = (DomainError, NotFoundError, PermissionDenied, AuthenticationError, ValidationError)
