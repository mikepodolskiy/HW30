from django.db import models

from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    name = models.CharField(max_length=140, unique=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

class User(AbstractUser):
    ROLE = [("member", "участник"), ("moderator", "модератор"), ("admin", "администратор")]

    role = models.CharField(max_length=9, choices=ROLE)
    age = models.PositiveSmallIntegerField(null=True)
    locations = models.ManyToManyField(Location)

    def save(self,*args, **kwargs):
        self.set_password(raw_password=self.password)
        super().save(*args, **kwargs)


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
# class User(AbstractUser):
#     MALE = 'm'
#     FEMALE = 'f'
#     SEX = [(MALE, "Male"), (FEMALE, "Female")]
#
#     HR = 'hr'
#     EMPLOYEE = 'employee'
#     UNKNOWN = 'unknown'
#     ROLE = [(HR, "hr"), (EMPLOYEE, "employee"), (UNKNOWN, "unknown")]
#
#     sex = models.CharField(max_length=1, choices=SEX, default=MALE)
#     role = models.CharField(max_length=8, choices=ROLE, default=UNKNOWN)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
