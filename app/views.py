from django.shortcuts import render
from .weather import *

from users.models import City, UserProfile

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

    hourly_data = hourly_weather(weather_data)
    context.update(hourly_data)

    daily_data = daily_weather(weather_data)
    context.update(daily_data)

    print(context)

    return render(request, "app/index.html", context=context)
