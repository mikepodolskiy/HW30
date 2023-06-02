from rest_framework.permissions import BasePermission

from ads.models import Ads


class AdUpdatePermission(BasePermission):
    message = "Ad update requires moderator permission"

    def has_permission(self, request, view):
        if request.role == "moderator":
            return True
        return False




class AdDeletePermission(BasePermission):
    message = "Ad delete requires moderator permission"

    def has_permission(self, request, view):
        if request.role == "moderator":
            return True
        return False


class AuthorCheckPermission(BasePermission):
    message = "Ad update or delete available only for ad's author"
    def has_permission(self, request, view):
        if request.user == Ads.objects.get("user"):
            return True
        return False
