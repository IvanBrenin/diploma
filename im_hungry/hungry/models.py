from django.db import models
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)


class Place(models.Model):
    name = models.CharField(max_length=128)
    specialization = models.CharField(max_length=128)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    place_photo = models.ImageField(upload_to='placephoto/')
    user_photo = models.ImageField(upload_to='userphoto/', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed', default=0)

    def __str__(self):
        return f'{self.specialization} - "{self.name}"'


class Good(models.Model):
    cls = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='pics/')
    rating = models.FloatField(null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='goods')
    price = models.FloatField()

    def __str__(self):
        return f'{self.place.name}: {self.cls} - {self.name}'


# class Price(models.Model):
#     place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='prices')
#     good = models.OneToOneField(Good, on_delete=models.CASCADE, related_name='price', null=True, blank=True)
#     price = models.FloatField()


class UserAddon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='addon')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

