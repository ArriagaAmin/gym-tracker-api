from api.models import Muscle
from api.repositories import MuscleRepository
from api.services.BaseService import BaseService


class MuscleService(BaseService[Muscle]):
    repository = MuscleRepository
