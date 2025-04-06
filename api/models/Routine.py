import uuid

from django.db import models

from .User import User


class Routine(models.Model):
    class RoutineStatus(models.IntegerChoices):
        ACTIVE = 0
        DELETED = 1

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.IntegerField(choices=RoutineStatus, default=RoutineStatus.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
