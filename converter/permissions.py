from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        print("testss")
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == str(request.user)