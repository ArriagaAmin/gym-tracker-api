from api.models import Exercise

from .BaseRepository import BaseRepository


class ExerciseRepository(BaseRepository[Exercise]):
    model = Exercise
