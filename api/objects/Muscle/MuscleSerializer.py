from rest_framework import serializers

from api.models import Muscle


class MuscleSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)

    class Meta:
        model = Muscle
        exclude = ("user",)
