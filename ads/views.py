# import required libraries and modules
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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

    def post(self, request):
        """
        method for add ad data
        :param request: request
        :return: saving new data to db
        """
        ad_data = json.loads(request.body)

        ad = Ads()

        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


# class for view of one element
class AdDetailView(View):

    def get(self, request, pk):
        """
       method for getting one element info
       :param request: request
       :param pk: required id
       :return: id, name, author, price, description, address, is_published in dict
       """
        ad = get_object_or_404(Ads, pk=pk)
        response = {
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# CBV for categories
@method_decorator(csrf_exempt, name="dispatch")
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

    def post(self, request):
        """
        method for add category data
        :param request: request
        :return: saving new data to db
        """
        category_data = json.loads(request.body)

        category = Categories()

        category.name = category_data["name"]

        category.save()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


# class for view of one element
class CategoryDetailView(View):

    def get(self, request, pk):
        """
        method for getting one element info
        :param request: request
        :param pk: required id
        :return: id, name in dict
        """
        category = get_object_or_404(Categories, pk=pk)
        response = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
