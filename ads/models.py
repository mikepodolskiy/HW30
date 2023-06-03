from django.db import models
from authentication.models import User


class Categories(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ads(models.Model):
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='logos/', blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class AdsSet(models.Model):
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ads = models.ManyToManyField(Ads)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def serialize(self):
        return {
            "id": self.id,
            "ads": [ad for ad in self.ads.all()],


        }
