# import required libraries and modules
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ads.models import Ads, Categories, AdsSet
from ads.permissions import IsAdminModer, IsAuthorPermission
from authentication.models import User
from ads.serializers import AdsListSerializer, AdDetailSerializer, AdUpdateSerializer, AdDeleteSerializer, \
    AdsSetListSerializer, AdsSetDetailSerializer, AdsSetCreateSerializer, AdsSetUpdateSerializer, AdsSetDeleteSerializer
from authentication.serializers import UserCreateSerializer


# start page using FBV
def index(request):
    return JsonResponse({"status": "OK"}, status=200)


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

        self.queryset = self.queryset.order_by("-price")

        return super().get(request, *args, **kwargs)

        # class for view of one element


class AdDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


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
class AdUpdateView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAdminModer, IsAuthorPermission]


# delete class for ads

class AdDeleteView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAdminModer, IsAuthorPermission]


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


# AdsSet views

class AdsSetListView(ListAPIView):
    queryset = AdsSet.objects.all()
    serializer_class = AdsSetListSerializer


class AdsSetDetailView(RetrieveAPIView):
    queryset = AdsSet.objects.all()
    serializer_class = AdsSetDetailSerializer


class AdsSetCreateView(CreateAPIView):
    queryset = AdsSet.objects.all()
    serializer_class = AdsSetCreateSerializer
    permission_classes = [IsAuthenticated]


class AdsSetUpdateView(UpdateAPIView):
    queryset = AdsSet.objects.all()
    serializer_class = AdsSetUpdateSerializer
    permission_classes = [IsAuthorPermission]


class AdsSetDeleteView(DestroyAPIView):
    queryset = AdsSet.objects.all()
    serializer_class = AdsSetDeleteSerializer
    permission_classes = [IsAuthorPermission]
