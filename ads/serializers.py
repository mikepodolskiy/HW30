from rest_framework import serializers

from ads.models import Location, User


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    locations = LocationCreateSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields = "__all__"
