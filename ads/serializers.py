from rest_framework import serializers

from ads.models import Ads, AdsSet


class AdsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Ads
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class AdsSetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSet
        fields = "__all__"


class AdsSetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSet
        fields = "__all__"


class AdsSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSet
        fields = "__all__"


class AdsSetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSet
        fields = "__all__"


class AdsSetDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSet
        fields = "__all__"
