from rest_framework import routers, serializers, viewsets
from api_v1.views import CharacterViewSet, UserViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet)
router.register("characters", CharacterViewSet)