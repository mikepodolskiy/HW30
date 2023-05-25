from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=140, unique=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

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
    locations = models.ManyToManyField("Location")


    def __str__(self):
        return self.username

    def serialize(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "role": self.role,
            "age": self.age,
            "locations": [location.name for location in self.locations.all()],

        }

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
