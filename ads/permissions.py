from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from ads.models import Ads
from authentication.models import User


class IsAdminModer(BasePermission):
    message = "Ad update requires admin/moderator permission"

    def has_permission(self, request, view):
        return request.user.role in ("admin", "moderator")


class IsAuthorPermission(BasePermission):
    message = "Action available only for author"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

