from django.shortcuts import render
import requests

from users.models import City, UserProfile

def index(request):
    if request.user.is_authenticated:
        city = City.objects.get(id =UserProfile.objects.get(user=request.user).city.id)
        context = {
            'city': city,
        }
    else:
        context = {
            'city': 'Gdańsk',
        }


    return render(request, "app/index.html", context=context)
