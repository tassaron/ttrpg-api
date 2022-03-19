from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from api_v1.views import CharacterViewSet


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router_v1 = routers.DefaultRouter(trailing_slash=False)
router_v1.register(r'users', UserViewSet)
router_v1.register(r'characters', CharacterViewSet)