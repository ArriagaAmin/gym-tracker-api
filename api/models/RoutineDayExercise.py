import uuid

from django.db import models

from api.utils import WeightUnit

from .RoutineDay import RoutineDay
from .Exercise import Exercise


class RoutineDayExercise(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    routine_day = models.ForeignKey(RoutineDay, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField(null=True, default=None)
    weight = models.DecimalField(null=True, decimal_places=2, max_digits=5, default=None)
    weight_unit = models.IntegerField(choices=WeightUnit, null=True, default=None)
    duration = models.DurationField(null=True, default=None)

    note = models.TextField()
