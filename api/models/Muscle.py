import uuid

from django.db import models

from .User import User


class Muscle(models.Model):
    class MuscleStatus(models.IntegerChoices):
        ACTIVE = 0
        DELETED = 1

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.IntegerField(choices=MuscleStatus, default=MuscleStatus.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
