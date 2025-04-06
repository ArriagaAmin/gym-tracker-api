from django.http import HttpRequest
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response as RestResponse

from api.controllers.BaseController import BaseController, controller, endpoint
from api.models import Exercise
from api.objects import (
    ExerciseInsertRequestDTO,
    ExerciseSerializer,
    ExerciseUpdateRequestDTO,
    Response,
)
from api.services import ExerciseService, UserService
from api.utils import first_non_none, raise_exception

@controller(route="exercise", name="Exercise")
class ExerciseController(BaseController):

    @staticmethod
    @endpoint(route="", methods=["POST"])
    def insert(http_request: HttpRequest):
        request = ExerciseInsertRequestDTO.model_validate_json(http_request.body)

        user = UserService.filter(id=request.user_id).first()
        if user is None:
            raise_exception("User", 1, user_id=request.user_id)

        exercise = Exercise(
            user=user,
            name=request.name,
            description=request.description,
            is_cardio=request.is_cardio,
        )
        exercise.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=ExerciseSerializer(exercise).data,
            ).to_dict(),
        )

    @staticmethod
    def update(http_request: HttpRequest, exercise: Exercise):
        request = ExerciseUpdateRequestDTO.model_validate_json(http_request.body)

        exercise.name = first_non_none(request.name, exercise.name)
        exercise.description = first_non_none(request.description, exercise.description)
        exercise.is_cardio = first_non_none(request.is_cardio, exercise.is_cardio)
        exercise.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=ExerciseSerializer(exercise).data,
            ).to_dict(),
        )

    @staticmethod
    def delete(exercise: Exercise):
        exercise.status = Exercise.ExerciseStatus.DELETED
        exercise.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=None,
            ).to_dict(),
        )

    @staticmethod
    @endpoint(route="<str:exercise_id>", methods=["PUT", "DELETE"])
    def one_exercise(http_request: HttpRequest, exercise_id: str):
        exercise = ExerciseService.filter(
            ~Q(status=Exercise.ExerciseStatus.DELETED),
            id=exercise_id,
        ).first()
        if exercise is None:
            raise_exception("Exercise", 1, exercise_id=exercise_id)

        if http_request.method == "PUT":
            return ExerciseController.update(http_request, exercise)
        elif http_request.method == "DELETE":
            return ExerciseController.delete(exercise)
