# import required libraries and modules
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ads, Categories


# start page using FBV
def index(request):
    return JsonResponse({"status": "OK"}, status=200)


# CBV for ads
class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        """
        method for getting all ads
        :param request: request
        :return: json response with data according to TDA
        """
        super().get(request, *args, **kwargs)

        response = [{
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        } for ad in self.object_list]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# class for view of one element
class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        """
       method for getting one element info
       :param request: request
       :return: id, name, author, price, description, address, is_published in dict
       """
        ad = self.get_object()
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


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ads
    fields = ["id", "name", "author", "price", "description", "address", "is_published"]

    def post(self, request, *args, **kwargs):
        """
        method for add ad data
        :param request: request
        :return: saving new data to db
        """
        ad_data = json.loads(request.body)

        ad = Ads.objects.create(
            name=ad_data["name"],
            author=ad_data["author"],
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


# update class for ads

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ads
    fields = ["id", "name", "author", "price", "description", "address", "is_published"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.id = ad_data["id"]
        self.object.name = ad_data["name"]
        self.object.author = ad_data["author"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.address = ad_data["address"]
        self.object.is_published = ad_data["is_published"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "address": self.object.address,
            "is_published": self.object.is_published,
        })


# delete class for ads

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ads
    success_url = "/"  # where to redirect after deleting

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# CBV for categories
class CategoriesListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        """
        method for getting all categories
        :param request: request
        :return: json response with data according to TDA
        """
        super().get(request, *args, **kwargs)

        response = [{
            "id": category.id,
            "name": category.name,
        } for category in self.object_list]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    # class for view of one element


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        """
        method for getting one element info
        :param request: request
        :return: id, name in dict
        """
        category = self.get_object()
        response = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Categories
    fields = ["id", "name"]

    def post(self, request, *args, **kwargs):
        """
        method for add category data
        :param request: request
        :return: saving new data to db
        """
        cat_data = json.loads(request.body)

        category = Categories.objects.create(
            name=cat_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


# update class for categories
@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ["id", "name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.id = cat_data["id"]
        self.object.name = cat_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


# delete class fo categories

@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = "/"  # where to redirect after deleting

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
