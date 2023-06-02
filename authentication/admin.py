from django.contrib import admin

from authentication.models import User, Location


admin.site.register(Location)
admin.site.register(User)
