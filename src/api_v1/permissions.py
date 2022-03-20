from rest_framework import permissions
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow admins
        if request.user.is_staff:
            return True

        if type(obj) == User:
            _id = obj.id
        else:
            _id = obj.user_id
        return _id == request.user.id