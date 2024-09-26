from rest_framework.permissions import BasePermission
from .constants import ADMIN, USER, ANALYST, DATA_VIEWER


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser or request.user.role == ADMIN


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == USER


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == ANALYST


class IsDataViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == DATA_VIEWER


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
