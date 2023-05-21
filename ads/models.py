from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=140, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class User(models.Model):
    ROLE = [("member", "участник"), ("moderator", "модератор"), ("admin", "администратор")]
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    username = models.CharField(max_length=140)
    password = models.CharField(max_length=140)
    role = models.CharField(max_length=9, choices=ROLE)
    age = models.PositiveSmallIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Categories(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ads(models.Model):
    name = models.CharField(max_length=140)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='logos/', blank=True, null=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
