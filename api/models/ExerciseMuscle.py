import uuid

from django.db import models

from .Exercise import Exercise
from .Muscle import Muscle


class ExerciseMuscle(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE)
