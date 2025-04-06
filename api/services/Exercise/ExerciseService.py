from api.models import Exercise
from api.repositories import ExerciseRepository
from api.services.BaseService import BaseService


class ExerciseService(BaseService[Exercise]):
    repository = ExerciseRepository
