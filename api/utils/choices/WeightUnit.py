from django.db import models


class WeightUnit(models.IntegerChoices):
    KG = 0
    LB = 1
