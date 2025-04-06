import uuid

from django.db import models

from .Routine import Routine


class RoutineDay(models.Model):
    class Day(models.IntegerChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    day = models.IntegerField(choices=Day)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["routine_id", "day"],
                name="unique_day_per_routine",
            ),
        ]
