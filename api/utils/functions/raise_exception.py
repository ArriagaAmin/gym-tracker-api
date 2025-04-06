from api.objects.GeneralException import GeneralException


UNKNOWN_ERROR = "Unknown error"

ERROR_CODES = {
    "Exercise": {
        1: "Exercise with ID {exercise_id} does not exists.",
    },
    "Muscle": {
        1: "Muscle with ID {muscle_id} does not exists.",
    },
    "User": {
        1: "User with ID {user_id} does not exists.",
    },
}

def raise_exception(model: str, error_num: int, **kwargs):
    message_template = ERROR_CODES.get(model, {}).get(error_num, UNKNOWN_ERROR)
    error_message = message_template.format(**kwargs)
    values = kwargs.values()

    raise GeneralException(
        code=f"{model}.{error_num}",
        messages=[error_message, *(str(v) for v in values)],
    )