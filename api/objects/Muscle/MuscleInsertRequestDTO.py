from pydantic import BaseModel
from typing_extensions import Annotated

from api.utils.functions.validators import is_uuid, min_len


class MuscleInsertRequestDTO(BaseModel):
    user_id: Annotated[str, is_uuid()]
    name: Annotated[str, min_len(3)]