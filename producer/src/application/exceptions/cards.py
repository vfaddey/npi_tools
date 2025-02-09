from src.application.exceptions.base import NPIToolsException


class NotACardOwner(NPIToolsException):
    ...


class SharingError(NPIToolsException):
    ...


class FailedToDeleteCard(NPIToolsException):
    ...