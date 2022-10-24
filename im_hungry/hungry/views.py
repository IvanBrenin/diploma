from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import generics
import random
import requests
import json

from .models import *
from .forms import *
from .serializers import *


GOOGLE_MAPS_API_KEY = 'AIzaSyCg-7rAL8j2eYd7NYQelNpdMR-mw0hoOZ0'


def index(request):
    context = {
        'best_places': sorted(Place.objects.all(), key=lambda d: -d.rating())[:3],
        'best_goods': sorted(Good.objects.all(), key=lambda d: -d.rating())[:4],
        'categories': Category.objects.all(),
        'michelin': {'stars': Place.michelin(), '66percent': (Place.michelin() / 3) * 2, '33percent': Place.michelin() / 3}
    }
    return render(request, template_name='hungry/index.html', context=context)


def register_user_page(request):
    form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, template_name='hungry/user_register.html', context=context)


@receiver(post_save, sender=User)
def create_user_addon(sender, instance, created, **kwargs):
    if created:
        UserAddon.objects.create(user=instance)


def add_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'avatar' in request.FILES:
                user.addon.avatar = request.FILES['avatar']
            if 'address' in request.POST:
                user.addon.address = request.POST['address']
            user.addon.save()
            return HttpResponseRedirect(reverse('hungry:registered'))
        else:
            context = {
                'message': 'There was an error. Try again!',
                'form': form,
            }
        return render(request, template_name='hungry/user_register.html', context=context)


def registered(request):
    form = PlaceForm()
    if request.method == 'POST':
        context = {
            'form': form,
        }
    else:
        context = {
            'message': 'Registration Sucessfully!'
        }
    return render(request, template_name='hungry/register_success.html', context=context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('hungry:index'))


def login_page(request):
    context = {
        'next_': request.POST['next_'],
    }
    return render(request, template_name='hungry/login_page.html', context=context)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_ = request.POST.get('next_')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        if next_:
            return HttpResponseRedirect(next_)
        else:
            return HttpResponseRedirect(reverse('hungry:index'))
    else:
        context = {
            'message': 'incorrect username or password'
        }
        if next_:
            context['next'] = next_
        return render(request, template_name='hungry/login_page.html', context=context)


def user_settings(request):
    return render(request, template_name='hungry/user_settings.html')


def distance(request, place_id):
    user = request.user
    place = Place.objects.filter(pk=place_id)
    return place.distance(user)


class PlaceListView(ListView):
    model = Place
    extra_context = {
         'michelin': {'stars': Place.michelin(), '66percent': (Place.michelin() / 3) * 2, '33percent': Place.michelin() / 3}
    }


def place_detail(request, place_id):
    user = request.user
    place = Place.objects.get(pk=place_id)
    if request.user.is_authenticated:
        adr = str(user.addon.address)
        target = str(place.geolocation)
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + adr + "&destinations=" + target + "&mode=walking&key=" + GOOGLE_MAPS_API_KEY
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        a = response.json()

        distance = a['rows'][0]['elements'][0]['distance']['text']
        time_to = a['rows'][0]['elements'][0]['duration']['text']

        context = {
            'place': place,
            'distance': distance,
            'time_to': time_to,
        }
    else:
        context = {
            'place': place,
            'message': 'Login to see distance!'
        }

    return render(request, template_name='hungry/place_detail.html', context=context)


def filter(request):
    filter_ = request.POST.get('filter')
    if filter_:
        goods_list = Good.objects.filter(cls__icontains=filter_)
        context = {
            'goods_list': goods_list
        }
        return render(request, template_name='hungry/search.html', context=context)
    if 'random' in request.POST:
        place_list = Place.objects.all()
        place = random.choice(place_list)
        return HttpResponseRedirect(reverse('hungry:place-detail', kwargs={'place_id': place.id}))
    if 'match' in request.POST:
        match = request.POST['match']
        place_list = Place.objects.filter(name__icontains=match)
        context = {
            'place_list': place_list,
            'michelin': {'stars': Place.michelin(), '66percent': (Place.michelin() / 3) * 2, '33percent': Place.michelin() / 3},
        }
        return render(request, template_name='hungry/search.html', context=context)


class CategoryDetailView(DetailView):
    model = Category
    extra_context = {
         'michelin': {'stars': Place.michelin(), '66percent': (Place.michelin() / 3) * 2, '33percent': Place.michelin() / 3},
    }


class GoodDetailView(DetailView):
    model = Good


def userphotos(request, place_id):
    place = Place.objects.get(pk=place_id)
    context = {
        'place': place,
    }
    return render(request, template_name='hungry/userphotos.html', context=context)


def add_or_remove_place_to_visited(request, place_id):
    user = request.user
    place = Place.objects.get(pk=place_id)
    if place not in user.visited.all():
        user.visited.add(place)
        place.visitors.add(user)
    else:
        user.visited.remove(place)
        place.visitors.remove(user)
    return HttpResponseRedirect(reverse('hungry:place-detail', kwargs={'place_id': place.id}))


def menu_edit_page(request, place_id):
    place = Place.objects.get(pk=place_id)
    form = GoodForm()
    context = {
        'place': place,
        'form': form,
    }
    return render(request, template_name='hungry/menu_editing.html', context=context)


def menu_edit(request, place_id):
    user = request.user
    place = Place.objects.get(pk=place_id)
    if request.user.is_authenticated:
        if user == place.manager:
            new_name = request.POST.get('new_name')
            new_price = request.POST.get('new_price')
            good = Good.objects.get(pk=request.POST['good_id'])
            if new_name:
                good.name = request.POST['new_name']
            if new_price:
                good.price = new_price
            if 'new_pic' in request.FILES:
                good.picture = request.FILES['new_pic']
            if 'new_desc' in request.FILES:
                good.description = request.FILES['new_desc']
            good.save()
            return HttpResponseRedirect(reverse('hungry:menu-edit-page', kwargs={'place_id': place.id}))
        else:
            context = {
                'message': 'You got to be place manager to do this!'
            }
            return render(request, template_name='hungry/menu_editing.html', context=context)
    else:
        context = {
            'message': 'You need to login to visit this page!'
        }
        return render(request, template_name='hungry/menu_editing.html', context=context)


def menu_add(request, place_id):
    user = request.user
    place = Place.objects.get(pk=place_id)
    if request.user.is_authenticated:
        if user == place.manager:
            if request.method == 'POST':
                form = GoodForm(request.POST, request.FILES)
                if form.is_valid():
                    new_good = form.save(commit=False)
                    if 'picture' in request.FILES:
                        new_good.picture = request.FILES['picture']
                    if 'plot' in request.FILES:
                        new_good.description = request.FILES['plot']
                    new_good.place = place
                    new_good.save()
            return HttpResponseRedirect(reverse('hungry:menu-edit-page', kwargs={'place_id': place.id}))
        else:
            context = {
                'message': 'You got to be place manager to do this!'
            }
            return render(request, template_name='hungry/menu_editing.html', context=context)
    else:
        context = {
            'message': 'You need to login to visit this page!'
        }
        return render(request, template_name='hungry/menu_editing.html', context=context)


def add_good_rating(request, good_id):
    user = request.user
    good = Good.objects.get(id__exact=good_id)
    if user not in good.rated_by.all():
        rating = request.POST['rate']
        new_rate = Rate(amount=rating, good=good, user=user)
        new_rate.save()
        user.rated.add(good)
        good.rated_by.add(user)
    else:
        rate = Rate.objects.get(user__exact=user, good__exact=good)
        rate.delete()
        user.rated.remove(good)
        good.rated_by.remove(user)
    return HttpResponseRedirect(reverse('hungry:good-detail', kwargs={'pk': good.id}))


def add_new_place(request):
    form = PlaceForm(request.POST, request.FILES)
    user = request.user
    adr = request.POST['address']
    if form.is_valid():
        new_place = form.save(commit=False)
        if 'place_photo' in request.FILES:
            new_place.place_photo = request.FILES['place_photo']
        new_place.manager = user
        new_place.geolocation = Place.geo(adr=adr)
        new_place.save()
        form.save_m2m()
    return HttpResponseRedirect(reverse('hungry:place-detail', kwargs={'place_id': new_place.id}))


def add_comment(request, place_id):
    user = request.user
    place = Place.objects.get(pk=place_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data.get('text')
        new_comment = PlaceComment(author=user, place=place, text=text)
        new_comment.save()
    return HttpResponseRedirect(reverse('hungry:place-detail', kwargs={'place_id': place.id}))


def user_detail(request, pk):
    user = User.objects.get(pk__exact=pk)
    context = {
        'object': user,
    }
    return render(request, template_name='hungry/user_detail.html', context=context)


def user_settings_apply(request):
    user = request.user
    if 'avatar' in request.FILES:
        user.addon.avatar = request.FILES['avatar']
    if 'address' in request.POST and len(request.POST['address']) > 2:
        user.addon.address = request.POST['address']
    user.addon.save()
    return HttpResponseRedirect(reverse('hungry:user-detail', kwargs={'pk': user.id}))


def place_photo_add(request, place_id):
    place = Place.objects.get(id__exact=place_id)
    if 'new_photo' in request.FILES:
        new_photo = UserPhoto(place=place, photo=request.FILES['new_photo'])
        new_photo.save()
    return HttpResponseRedirect(reverse('hungry:place-detail', kwargs={'place_id': place.id}))


class PlaceListAPIView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer1


class GoodListAPIView(generics.ListAPIView):
    queryset = Good.objects.order_by('-place')
    serializer_class = GoodSerializer1
