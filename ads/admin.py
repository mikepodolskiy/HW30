from django.contrib import admin

from ads.models import Ads, Categories, Location, User

admin.site.register(Ads)
admin.site.register(Categories)
admin.site.register(Location)
admin.site.register(User)
