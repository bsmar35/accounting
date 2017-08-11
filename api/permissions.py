from api.models import Account, Manager
from rest_framework import permissions


class AccountOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return isinstance(obj.owner, Account)


class ManagerOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return isinstance(obj.owner, Manager)
