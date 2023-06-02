from rest_framework import serializers

from ads.models import Ads


class AdsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Ads
        fields = "__all__"


