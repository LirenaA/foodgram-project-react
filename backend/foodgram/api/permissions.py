from rest_framework import permissions


class CanViewAnyObject(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        return request.user.is_authenticated and request.method == 'GET'

class CustomUserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_authenticated
        return True


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
