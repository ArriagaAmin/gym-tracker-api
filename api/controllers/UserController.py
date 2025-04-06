from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response as RestResponse

from api.controllers.BaseController import BaseController, controller, endpoint
from api.models import Exercise, Muscle, User
from api.objects import (
    ExerciseSerializer,
    MuscleSerializer,
    Response,
    UserInsertRequestDTO,
    UserSerializer,
)
from api.services import ExerciseService, MuscleService, UserService
from api.utils import raise_exception


@controller(route="user", name="User")
class UserController(BaseController):

    @staticmethod
    def insert(http_request: HttpRequest):
        request = UserInsertRequestDTO.model_validate_json(http_request.body)

        user = User(name=request.name)
        user.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=UserSerializer(user).data,
            ).to_dict(),
        )

    @staticmethod
    def get_all():
        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=UserSerializer(UserService.all(), many=True).data,
            ).to_dict(),
        )

    @staticmethod
    @endpoint(route="", methods=["GET", "POST"])
    def all_users(http_request: HttpRequest):
        if http_request.method == "GET":
            return UserController.get_all()
        elif http_request.method == "POST":
            return UserController.insert(http_request)

    @staticmethod
    @endpoint(route="<str:user_id>/exercise", methods=["GET"])
    def get_all_exercises(http_request: HttpRequest, user_id: str):
        user = UserService.filter(id=user_id).first()
        if user is None:
            raise_exception("User", 1, user_id=user_id)

        user_exercises = ExerciseService.filter(
            user_id=user_id,
            status=Exercise.ExerciseStatus.ACTIVE,
        )

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=ExerciseSerializer(user_exercises, many=True).data,
            ).to_dict(),
        )

    @staticmethod
    @endpoint(route="<str:user_id>/muscle", methods=["GET"])
    def get_all_muscles(http_request: HttpRequest, user_id: str):
        user = UserService.filter(id=user_id).first()
        if user is None:
            raise_exception("User", 1, user_id=user_id)

        user_muscles = MuscleService.filter(
            user_id=user_id,
            status=Muscle.MuscleStatus.ACTIVE,
        )

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=MuscleSerializer(user_muscles, many=True).data,
            ).to_dict(),
        )
