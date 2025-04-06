import pytest
from django.test import Client
from api.repositories import UserRepository

@pytest.fixture(scope="session")
def client():
    return Client()

@pytest.fixture(scope="function")
def user():
    return UserRepository.create(name="Test User")
