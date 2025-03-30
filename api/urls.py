from api.controllers import UserController

urlpatterns = [
    *UserController.get_paths(),
]