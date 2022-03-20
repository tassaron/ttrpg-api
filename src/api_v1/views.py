from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions
from rest_framework.reverse import reverse_lazy
from rest_framework.response import Response
from .models import Character
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, CharacterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Create a new user account by sending a POST request. Email is optional. Password will be re-hashed if changed in a PUT/PATCH request
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        all_data = []
        for row in self.queryset:
            serializer = self.serializer_class(row, context={'request': request})
            data = serializer.data
            del data["password"]
            del data["email"]
            all_data.append(data)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, context={'request': request})
        data = serializer.data
        del data["password"]
        del data["email"]
        return Response(data)


class CharacterViewSet(viewsets.ModelViewSet):
    """
    "Data" must be a string repr of a Python dict
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request):
        all_data = []
        for row in self.queryset:
            serializer = self.serializer_class(row, context={'request': request})
            data = serializer.data
            data.update({
                "url": reverse_lazy('v1:character-detail', args=[row.id], request=request)
            })
            all_data.append(data)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        serializer = self.serializer_class(character, context={'request': request})
        data = serializer.data
        data.update({
            "url": reverse_lazy('v1:character-detail', args=[pk], request=request)
        })
        return Response(data)

    def create(self, request):
        request.data["user_id"] = request.user.id
        serializer = self.serializer_class(self.queryset, context={'request': request})
        data = serializer.validate(request.data)
        instance = serializer.create(data)
        return Response(self.serializer_class(instance).data)
