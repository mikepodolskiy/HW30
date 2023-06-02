# import required libraries and modules
import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from HW27 import settings

from authentication.models import User, Location
from authentication.serializers import UserCreateSerializer, LocationListSerializer


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


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# update class for ads

@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

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
        self.object.save()

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
