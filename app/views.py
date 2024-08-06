from django.shortcuts import render
import requests
import openmeteo_requests
from retry_requests import retry
import requests_cache
from .weather import *

from users.models import City, UserProfile


# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)
#

def index(request):
    if request.user.is_authenticated:
        city = City.objects.get(id=UserProfile.objects.get(user=request.user).city.id)
    else:
        city = City.objects.get(city="Gdańsk")

    latitude = city.latitude
    longitude = city.longitude

    context = {
        'city': city,
        'latitude': latitude,
        'longitude': longitude,
    }

    weather_data = get_weather(latitude, longitude)
    current_data = current_weather(weather_data)
    context.update(current_data)

    print(context)

    return render(request, "app/index.html", context=context)
