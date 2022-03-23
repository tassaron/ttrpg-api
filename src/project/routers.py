from rest_framework import routers, serializers, viewsets
from api.views import CharacterViewSet, UserViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet)
router.register("characters", CharacterViewSet)
router.get_api_root_view().cls.__name__ = "root"
router.get_api_root_view().cls.__doc__ = "Create a new user account by sending a POST request to /users, then authenticate to use the API"