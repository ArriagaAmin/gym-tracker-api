from pydantic import BaseModel
from typing_extensions import Annotated

from api.utils.functions.validators import min_len


class MuscleUpdateRequestDTO(BaseModel):
    name: Annotated[str | None, min_len(3)] = None
