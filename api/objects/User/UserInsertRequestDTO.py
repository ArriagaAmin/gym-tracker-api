from pydantic import BaseModel
from typing_extensions import Annotated

from api.utils.functions.validators import min_len


class UserInsertRequestDTO(BaseModel):
    name: Annotated[str, min_len(3)]
