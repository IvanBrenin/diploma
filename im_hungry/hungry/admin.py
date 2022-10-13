from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from .models import *


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


# @admin.register(Price)
# class PriceAdmin(admin.ModelAdmin):
#     pass


@admin.register(UserAddon)
class UserAddonAdmin(admin.ModelAdmin):
    pass
