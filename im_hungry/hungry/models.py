from django.db import models
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

import requests
import json

GOOGLE_MAPS_API_KEY = 'AIzaSyCg-7rAL8j2eYd7NYQelNpdMR-mw0hoOZ0'

class Category(models.Model):
    name = models.CharField(max_length=128)
    cat_pic = models.ImageField(upload_to='categorypics/', null=True, blank=True)
    # places

    def __str__(self):
        return self.name

    def url(self):
        return reverse('hungry:category-detail', kwargs={'pk': self.id})


class Place(models.Model):
    name = models.CharField(max_length=128)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100, null=True, blank=True)
    place_photo = models.ImageField(upload_to='placephoto/')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='managed', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='places', null=True, blank=True)
    visitors = models.ManyToManyField(User, related_name='visited', blank=True)
    # userphotos

    def __str__(self):
        return f'{self.category} - "{self.name}"'

    def rating(self):
        goods = self.goods.all()
        rate = 0
        if goods:
            for i in goods:
                a = i.rating()
                if a <= 2:
                    rate -= a
                else:
                    rate += a
            if rate >= 0:
                return rate
            else:
                return 0.0
        return 0.0

    def url(self):
        return reverse('hungry:place-detail', kwargs={'pk': self.id})

    @staticmethod
    def geo(adr):
        adr = adr
        url = "https://maps.google.com/maps/api/geocode/json?address=" + adr + "&key=" + GOOGLE_MAPS_API_KEY
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        a = response.json()
        return (str(a['results'][0]['geometry']['location']['lat']) + ',' + str(
            a['results'][0]['geometry']['location']['lng']))

    @staticmethod
    def michelin():
        a = max(Place.objects.all(), key=lambda d: d.rating())
        return a.rating()


    # def manager(self):
    #     return self.manager


class Good(models.Model):
    cls = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='pics/')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='goods')
    price = models.FloatField()
    rating = models.FloatField(default=0, null=True, blank=True)
    description = models.FileField(upload_to='desc/', null=True, blank=True)
    rated_by = models.ManyToManyField(User, related_name='rated', blank=True)
    # ratings


    def __str__(self):
        return f'{self.place.name}: {self.cls} - {self.name}'

    def url(self):
        return reverse('hungry:good-detail', kwargs={'pk': self.id})

    def rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.amount for r in ratings) / len(ratings)
        return 0.0



class UserAddon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='addon')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    address = map_fields.AddressField(max_length=200, null=True, blank=True)


class UserPhoto(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='userphotos')
    photo = models.FileField(upload_to='userphotos/', null=True, blank=True)


class Rate(models.Model):
    amount = models.IntegerField(null=True, blank=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)


class PlaceComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')
    dislikes = models.ManyToManyField(User, blank=True, related_name='disliked')

    def __str__(self):
        return f'{self.text} ({self.place})'

    class Meta:
        ordering = ['-published']