from uuid import UUID

from pydantic.functional_validators import AfterValidator


def is_uuid():
    def check(value: str | None):
        if value is None:
            return None
        try:
            UUID(value, version=4)
        except:
            raise ValueError(f"'{value}' is not a valid UUID")
        return value

    return AfterValidator(check)

def min_len(min_length: int):
    def check(value: str | None):
        if value is None: 
            return None
        if len(value) < min_length:
            raise ValueError(f"'{value}' is too short, must be at least {min_length} characters long")
        return value

    return AfterValidator(check)
