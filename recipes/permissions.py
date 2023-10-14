from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Permission class to check if the user requesting the object is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Allows read-only access to unauthenticated users, and allows write access to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )