from django.http import HttpRequest
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response as RestResponse

from api.controllers.BaseController import BaseController, controller, endpoint
from api.models import Muscle
from api.objects import (
    MuscleInsertRequestDTO,
    MuscleSerializer,
    MuscleUpdateRequestDTO,
    Response,
)
from api.services import MuscleService, UserService
from api.utils import first_non_none, raise_exception

@controller(route="muscle", name="Muscle")
class MuscleController(BaseController):

    @staticmethod
    @endpoint(route="", methods=["POST"])
    def insert(http_request: HttpRequest):
        request = MuscleInsertRequestDTO.model_validate_json(http_request.body)

        user = UserService.filter(id=request.user_id).first()
        if user is None:
            raise_exception("User", 1, user_id=request.user_id)

        muscle = Muscle(user=user, name=request.name)
        muscle.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=MuscleSerializer(muscle).data,
            ).to_dict(),
        )

    @staticmethod
    def update(http_request: HttpRequest, muscle: Muscle):
        request = MuscleUpdateRequestDTO.model_validate_json(http_request.body)

        muscle.name = first_non_none(request.name, muscle.name)
        muscle.save()

        return RestResponse(
            status=status.HTTP_200_OK,
            data=Response(
                code=0,
                error=False,
                messages=[f"Success"],
                data=MuscleSerializer(muscle).data,
            ).to_dict(),
        )

    @staticmethod
    def delete(muscle: Muscle):
        muscle.status = Muscle.MuscleStatus.DELETED
        muscle.save()

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
    @endpoint(route="<str:muscle_id>/", methods=["PUT", "DELETE"])
    def one_muscle(http_request: HttpRequest, muscle_id: str):
        muscle = MuscleService.filter(
            ~Q(status=Muscle.MuscleStatus.DELETED),
            id=muscle_id,
        ).first()
        if muscle is None:
            raise_exception("Muscle", 1, muscle_id=muscle_id)

        if http_request.method == "PUT":
            return MuscleController.update(http_request, muscle)
        elif http_request.method == "DELETE":
            return MuscleController.delete(muscle)
