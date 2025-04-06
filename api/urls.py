from api.controllers import (
    HealthCheckController,
    ExerciseController,
    MuscleController,
    UserController,
)

urlpatterns = [
    *HealthCheckController.get_paths(),
    *ExerciseController.get_paths(),
    *MuscleController.get_paths(),
    *UserController.get_paths(),
]
