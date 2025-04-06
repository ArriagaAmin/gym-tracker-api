from uuid import uuid4
import pytest

from django.test import Client

from api.models import Muscle, User
from api.repositories import MuscleRepository


class MuscleControllerTest:

    @pytest.fixture(scope="class")
    def base_path(self):
        return "/api/muscle"

    @pytest.fixture(scope="function")
    def muscle(self, user: User):
        return Muscle(user=user, name="Biceps")

    @pytest.fixture(scope="function")
    def db_muscle(self, user: User):
        return MuscleRepository.create(
            user=user,
            name="Shoulders",
        )


    @pytest.mark.django_db
    def test_insert_failure_user_not_found(
        self,
        client: Client,
        base_path: str,
        muscle: Muscle,
    ):
        url = f"{base_path}/"
        data = {"user_id": uuid4(), "name": muscle.name}

        response = client.post(url, data, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "User.1"

    @pytest.mark.django_db
    def test_insert_success(self, client: Client, base_path: str, muscle: Muscle):
        url = f"{base_path}/"
        data = {"user_id": muscle.user.id, "name": muscle.name}

        response = client.post(url, data, content_type="application/json")
        data = response.json()
        new_muscle = data["data"]

        assert response.status_code == 200
        assert data["error"] == False
        assert new_muscle["name"] == muscle.name
        assert new_muscle["user_id"] == str(muscle.user.id)

    @pytest.mark.django_db
    def test_update_failure_muscle_not_found(self, client: Client, base_path: str):
        url = f"{base_path}/{uuid4()}/"
        data = {}

        response = client.put(url, data, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "Muscle.1"

    @pytest.mark.django_db
    def test_update_failure_muscle_deleted(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"
        data = {}

        db_muscle.status = Muscle.MuscleStatus.DELETED
        db_muscle.save()

        response = client.put(url, data, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "Muscle.1"

    @pytest.mark.django_db
    def test_update_failure_name_too_short(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"
        data = {"name": "T"}

        response = client.put(url, data, content_type="application/json")
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "Validation"

    @pytest.mark.django_db
    def test_update_success_without_changes(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"
        data = {}

        response = client.put(url, data, content_type="application/json")
        data = response.json()
        updated_muscle = data["data"]

        assert response.status_code == 200
        assert data["error"] == False
        assert updated_muscle["id"] == str(db_muscle.id)
        assert updated_muscle["name"] == db_muscle.name

    @pytest.mark.django_db
    def test_update_success_with_changes(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"
        new_name = "Triceps"
        data = {"name": new_name}

        response = client.put(url, data, content_type="application/json")
        data = response.json()
        updated_muscle = data["data"]

        assert response.status_code == 200
        assert data["error"] == False
        assert updated_muscle["id"] == str(db_muscle.id)
        assert updated_muscle["name"] == new_name

    @pytest.mark.django_db
    def test_delete_failure_muscle_not_found(self, client: Client, base_path: str):
        url = f"{base_path}/{uuid4()}/"

        response = client.delete(url, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "Muscle.1"

    @pytest.mark.django_db
    def test_delete_failure_muscle_deleted(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"

        db_muscle.status = Muscle.MuscleStatus.DELETED
        db_muscle.save()

        response = client.delete(url, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == True
        assert data["code"] == "Muscle.1"

    @pytest.mark.django_db
    def test_delete_success(
        self,
        client: Client,
        base_path: str,
        db_muscle: Muscle,
    ):
        url = f"{base_path}/{db_muscle.id}/"

        response = client.delete(url, content_type="application/json")
        data = response.json()

        assert response.status_code == 200
        assert data["error"] == False
        assert MuscleRepository.get(db_muscle.id).status == Muscle.MuscleStatus.DELETED
