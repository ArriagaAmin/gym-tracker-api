from api.models import Muscle

from .BaseRepository import BaseRepository


class MuscleRepository(BaseRepository[Muscle]):
    model = Muscle
