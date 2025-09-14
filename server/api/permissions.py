from typing import override

from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Author can change own instances, other read only."""

    @override
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True

    @override
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_superuser or obj.user == request.user)
