from rest_framework import serializers
from .models import *


class PlaceSerializer1(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()
    class Meta:
        model = Place
        fields = ['id', 'category', 'name', 'address', 'manager', 'place_photo']


class GoodSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['cls', 'name', 'place', 'price', 'picture']