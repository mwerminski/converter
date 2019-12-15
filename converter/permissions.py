from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsOwner(permissions.BasePermission):
    raise_not_found_for_methods = []
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.owner == str(request.user): return True
        else: raise exceptions.PermissionDenied