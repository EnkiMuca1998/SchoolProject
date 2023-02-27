from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, BasePermission

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
