from django.test import TestCase

from .models import *

class PlaceModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Place.objects.create(name='McDonalds', address='Obolonsky Ave Kyiv Ukraine')

    def test1(self):
        place = Place.objects.get(id__exact=1)
        s1 = self.category + ' - "' + self.name + '"'
        s2 = str(place)
        self.assertEqual(s1, s2)