from rest_framework.permissions import *
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCurrentUserObject(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsSuperUserORIsCurrentUserObject(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user") and obj.user:
            return obj.user == request.user or request.user.is_superuser
        return obj == request.user or request.user.is_superuser


class IsCurrentUserObjectOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj == request.user


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.method in SAFE_METHODS
