class ValidationException(Exception):
    pass


def guard_alphanumeric(string: str, message: str):
    if not string.isalnum():
        raise ValidationException(message)
