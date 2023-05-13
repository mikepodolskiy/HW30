# import required libraries and modules
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.models import Ads, Categories

# start page using FBV
def index(request):
    return JsonResponse({"status": "OK"}, status=200)

# CBV for ads
@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):

    def get(self, request):
        """
        method for getting all ads
        :param request: request
        :return: json response with data according to TDA
        """
        if request.method == "GET":
            ads = Ads.objects.all()
            response = [{
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            } for ad in ads]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

# CBV for categories
class CategoriesView(View):

    def get(self, request):
        """
        method for getting all categories
        :param request: request
        :return: json response with data according to TDA
        """
        if request.method == "GET":
            categories = Categories.objects.all()
            response = [{
                "id": category.id,
                "name": category.name,
            } for category in categories]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
