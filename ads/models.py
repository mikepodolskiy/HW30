from django.db import models


class Ads(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)
    author = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=280)
    is_published = models.BooleanField()

    def __str__(self):
        return self.name


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name
