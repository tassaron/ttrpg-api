from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.reverse import reverse_lazy
from rest_framework.response import Response
from .models import Character
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, CharacterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        """Create a new user account by sending a POST request. Email is optional."""
        all_data = []
        for row in self.queryset:
            serializer = self.serializer_class(row, context={'request': request})
            data = serializer.data
            del data["password"]
            del data["email"]
            data.update({
                "characters": reverse_lazy('v1:user-characters', args=[row.id], request=request)
            })
            all_data.append(data)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        """Password will be re-hashed if changed in a PUT/PATCH request"""
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, context={'request': request})
        data = serializer.data
        del data["password"]
        del data["email"]
        data.update({
            "characters": reverse_lazy('v1:user-characters', args=[pk], request=request)
        })
        return Response(data)

    @action(detail=True)
    def characters(self, request, *args, **kwargs):
        """Character sheets created by this user"""
        obj = self.get_object()
        queryset = Character.objects.filter(user_id=obj.id).all()
        all_data = []
        for row in queryset:
            serializer = CharacterSerializer(row, context={'request': request})
            data = serializer.data
            del data["user_id"]
            data.update({
                "url": reverse_lazy('v1:character-detail', args=[row.id], request=request)
            })
            all_data.append(data)
        return Response(all_data)


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
            del data["user_id"]
            data.update({
                "user": reverse_lazy('v1:user-detail', args=[row.user_id], request=request),
                "url": reverse_lazy('v1:character-detail', args=[row.id], request=request),
            })
            all_data.append(data)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        character = get_object_or_404(Character, pk=pk)
        serializer = self.serializer_class(character, context={'request': request})
        data = serializer.data
        data.update({
            "user": reverse_lazy('v1:user-detail', args=[data["user_id"]], request=request),
            "url": reverse_lazy('v1:character-detail', args=[pk], request=request)
        })
        del data["user_id"]
        return Response(data)

    def create(self, request):
        request.data["user_id"] = request.user.id
        serializer = self.serializer_class(self.queryset, context={'request': request})
        data = serializer.validate(request.data)
        instance = serializer.create(data)
        return Response(self.serializer_class(instance).data)
