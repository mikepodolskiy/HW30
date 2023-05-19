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

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=140)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=8, decimal_places=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class User(models.Model):
    ROLE = [("member", "участник"), ("moderator", "модератор"), ("admin", "администратор")]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    username = models.CharField(max_length=140)
    password = models.CharField(max_length=140)
    role = models.CharField(max_length=140, choices=ROLE)
    age = models.PositiveSmallIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
