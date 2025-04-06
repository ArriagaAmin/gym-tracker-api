import uuid

from django.db import models

from .User import User


class RoutineDayLog(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "date"],
                name="unique_date_per_routine_log",
            ),
        ]
