from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from ads.models import Ads
from authentication.models import User


class IsAdminModer(BasePermission):
    message = "Ad update requires admin/moderator permission"

    def has_permission(self, request, view):
        return request.user.role in ("admin", "moderator")

class IsAuthorPermission(BasePermission):
    message = "Ad update or delete available only for ad's author"

    def has_permission(self, request, view):
        if request.user.username == Ads.objects.get("user"):
            return True
        return False
