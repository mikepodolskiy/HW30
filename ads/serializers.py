from rest_framework import serializers

from ads.models import Ads
from authentication.models import User, Location


class AdsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Ads
        fields = "__all__"


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Location
        fields = "__all__"


class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    locations = LocationCreateSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
