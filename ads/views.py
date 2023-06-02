# import required libraries and modules
import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from HW27 import settings
from ads.models import Ads, Categories
from authentication.models import User, Location
from ads.serializers import UserCreateSerializer, LocationListSerializer, LocationDetailSerializer, \
    LocationCreateSerializer, LocationUpdateSerializer, LocationDeleteSerializer, AdsListSerializer


# start page using FBV
def index(request):
    return JsonResponse({"status": "OK"}, status=200)


# CBV for ads
# class AdsListView(ListView):
#     model = Ads
#     queryset = Ads.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         """
#         method for getting all ads
#         :param request: request
#         :return: json response with data according to TDA
#         """
#         super().get(request, *args, **kwargs)
#
#         # sorting
#         self.object_list = self.object_list.order_by("-price")
#
#         # pagination
#         paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
#         page_num = request.GET.get("page")
#         page_obj = paginator.get_page(page_num)
#         ads = [{
#             "id": ad.id,
#             "name": ad.name,
#             "user": ad.user.id,
#             "price": ad.price,
#             "description": ad.description,
#             "is_published": ad.is_published,
#             "image": ad.image.url,
#             "category": ad.category.id
#         } for ad in page_obj]
#
#         # forming response
#         response = [{
#             "items": ads,
#             "total": paginator.count,
#             "num_pages": paginator.num_pages
#         }]
#
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class AdsListView(ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsListSerializer

    def get(self, request, *args, **kwargs):

        # filter by name of ad
        ad_text = request.GET.get("text", None)
        if ad_text:
            self.queryset = self.queryset.filter(name__icontains=ad_text)

        # filter by category of ad
        cats = request.GET.getlist("cat", None)
        cats_query = None
        for cat in cats:
            if cats_query is None:
                cats_query = Q(category__id__exact=cat)
            else:
                cats_query |= Q(category__id__exact=cat)
        if cats_query:
            self.queryset = self.queryset.filter(cats_query)

        # filter by location of ad
        location = request.GET.get("location", None)

        if location:
            self.queryset = self.queryset.filter(user__locations__name__icontains=location)

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from and price_from.is_digit():
            self.queryset = self.queryset.filter(price__gte=price_from)

        # filter by price of ad
        if price_to and price_to.is_digit():
            self.queryset = self.queryset.filter(price__lte=price_from)

        self.queryset = self.queryset.order_by(("-price"))

        return super().get(request, *args, **kwargs)

        # class for view of one element


class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        """
       method for getting one element info
       :param request: request
       :return: id, name, user, price, description, address, is_published in dict
       """
        ad = self.get_object()
        response = {
            "id": ad.id,
            "name": ad.name,
            "user": ad.user.id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category": ad.category.id
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ads
    fields = "__all__"
    def post(self, request, *args, **kwargs):
        """
        method for add ad data
        :param request: request
        :return: saving new data to db
        """
        ad_data = json.loads(request.body)

        # getting objects from another instances, which are used as source of data
        user = get_object_or_404(User, pk=ad_data.get("user"))
        category = get_object_or_404(Categories, pk=ad_data.get("user"))

        ad = Ads.objects.create(
            name=ad_data["name"],
            user=user,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            image=ad_data["image"],
            category=category,
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "user": ad.user.id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url,
            "category": ad.category.id
        })


# update class for ads

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ads
    fields = ["id", "name", "user", "price", "description", "is_published", "image", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        # getting data from request
        ad_data = json.loads(request.body)

        # checking what data are in request and set new object data, request to another instances if required
        if "name" in ad_data:
            self.object.name = ad_data["name"]
        if "user" in ad_data:
            user = get_object_or_404(User, pk=ad_data.get("user"))
            self.object.user = user
        if "price" in ad_data:
            self.object.price = ad_data["price"]
        if "description" in ad_data:
            self.object.description = ad_data["description"]
        if "image" in ad_data:
            self.object.image = ad_data["image"]
        if "is_published" in ad_data:
            self.object.is_published = ad_data["is_published"]
        if "category" in ad_data:
            category = get_object_or_404(Categories, pk=ad_data.get("category"))
            self.object.category = category

        # save data to db
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "user": self.object.user.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url,
            "category": self.object.category.id
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
    fields = ["id", "name", "user", "price", "description", "address", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["logo"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "user_id": self.object.user.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category_id": self.object.category.id
        })


# CBV for categories
class CategoriesListView(ListView):
    model = Categories
    queryset = Categories.objects.all()

    def get(self, request, *args, **kwargs):
        """
        method for getting all categories
        :param request: request
        :return: json response with data according to TDA
        """
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

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


# CRUD for User
class UserListView(ListView):
    model = User
    queryset = User.objects.prefetch_related("locations").annotate(
        total_ads=Count("ads", filter=Q(ads__is_published=True)))

    def get(self, request, *args, **kwargs):
        """
        method for getting all users
        :param request: request
        :return: json response with data according to TDA
        """
        super().get(request, *args, **kwargs)
        # sorting
        self.object_list = self.object_list.order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)

        response = [{
            "items": [user.serialize() for user in page_obj],
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# class for view of one element
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        """
       method for getting one element info
       :param request: request
       :return: data according to TDA
       """
        user = self.get_object()
        # counting by ads

        return JsonResponse(user.serialize(), safe=False, json_dumps_params={"ensure_ascii": False})


# @method_decorator(csrf_exempt, name="dispatch")
# class UserCreateView(CreateView):
#     model = User
#     fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "locations"]
#
#     def post(self, request, *args, **kwargs):
#         """
#         method for add ad data
#         :param request: request
#         :return: saving new data to db
#         """
#         user_data = json.loads(request.body)
#
#         locations = user_data.pop("locations")
#         user = User.objects.create(**user_data)
#
#         for location_name in locations:
#             loc, created = Location.objects.get_or_create(name=location_name)
#             user.locations.add(loc)
#
#         return JsonResponse(user.serialize())

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# update class for ads

@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["id", "first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        if "first_name" in user_data:
            self.object.first_name = user_data["first_name"]
        if "last_name" in user_data:
            self.object.last_name = user_data["last_name"]
        if "username" in user_data:
            self.object.username = user_data["username"]
        if "password" in user_data:
            self.object.password = user_data["password"]
        if "role" in user_data:
            self.object.role = user_data["role"]
        if "age" in user_data:
            self.object.age = user_data["age"]
        if "locations" in user_data:
            locations = user_data.get("locations")
            for location_name in locations:
                loc, created = Location.objects.get_or_create(name=location_name)
                self.object.locations.add(loc)

        return JsonResponse(self.object.serialize())


# delete class for ads

@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"  # where to redirect after deleting

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# Location views with DRF

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer

#
# class LocationDetailView(RetrieveAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationDetailSerializer
#
#
# class LocationCreateView(CreateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationCreateSerializer
#
#
# class LocationUpdateView(UpdateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationUpdateSerializer
#
#
# class LocationDeleteView(DestroyAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationDeleteSerializer

################################################################
# class LocationListView(ListView):
#     model = Location
#
#     def get(self, request, *args, **kwargs):
#         """
#         method for getting all ads
#         :param request: request
#         :return: json response with data according to TDA
#         """
#         super().get(request, *args, **kwargs)
#
#         response = [{
#             "name": loc.name,
#             "lat": loc.lat,
#             "lng": loc.lng
#         } for loc in self.object_list]
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class LocationCreateView(CreateView):
#     model = Location
#     fields = ["id", "name", "lat", "lng"]
#
#     def post(self, request, *args, **kwargs):
#         """
#         method for add location data
#         :param request: request
#         :return: saving new data to db
#         """
#         location_data = json.loads(request.body)
#
#         location = Location.objects.create(
#             name=location_data["name"],
#             lat=location_data["lat"],
#             lng=location_data["lng"],
#         )
#         return JsonResponse({
#             "name": location.name,
#             "lat": location.lat,
#             "lng": location.lng,
#         })
##################################################################
