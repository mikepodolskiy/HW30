# import required libraries and modules
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from HW27 import settings
from ads.models import Ads, Categories, User


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
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)
        ads = [{
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id.id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category_id": ad.category_id.id
        } for ad in page_obj]

        response = [{
            "items": ads,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }]

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
            "author_id": ad.author_id.id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category_id": ad.category_id.id
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ads
    fields = ["id", "name", "author_id", "price", "description", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        """
        method for add ad data
        :param request: request
        :return: saving new data to db
        """
        ad_data = json.loads(request.body)

        author_id = get_object_or_404(User, pk=ad_data.get("author_id"))
        category_id = get_object_or_404(Categories, pk=ad_data.get("author_id"))


        ad = Ads.objects.create(
            name=ad_data["name"],
            author_id=author_id,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            image=ad_data["image"],
            category_id=category_id,
        )



        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id.id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category_id": ad.category_id.id
        })


# update class for ads

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ads
    fields = ["id", "name", "author_id", "price", "description", "is_published", "image", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if "name" in ad_data:
            self.object.name = ad_data["name"]
        if "author_id" in ad_data:
            author_id = get_object_or_404(User, pk=ad_data.get("author_id"))
            self.object.author_id = author_id
        if "price" in ad_data:
            self.object.price = ad_data["price"]
        if "description" in ad_data:
            self.object.description = ad_data["description"]
        if "image" in ad_data:
            self.object.image = ad_data["image"]
        if "is_published" in ad_data:
            self.object.is_published = ad_data["is_published"]
        if "category_id" in ad_data:
            category_id = get_object_or_404(Categories, pk=ad_data.get("category_id"))
            self.object.category_id = category_id

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": author_id.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url,
            "category_is": category_id.id
        })


# delete class for ads

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ads
    success_url = "/"  # where to redirect after deleting

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# add logo class
@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ads
    fields = ["id", "name", "author_id", "price", "description", "address", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["logo"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category_id": self.object.category_id.id
        })


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
