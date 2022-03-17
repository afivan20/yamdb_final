from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework import permissions


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_admin
        return False


class IsAdminUserOrReadOnlyGenCat(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if (request.method == 'POST'
                    or request.method == 'PUT'
                    or request.method == 'PATCH'
                    or request.method == 'DELETE'):
                return request.user.is_admin
        return False


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsAuthorOrReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminModeratorAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_moderator)
