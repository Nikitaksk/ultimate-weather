import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .weather import *

from users.models import City, UserProfile


def index(request, searched_city=None):
    if searched_city:
        try:
            city = City.objects.filter(name=searched_city.capitalize())[0]
        except Exception as e:
            return redirect("index")
    elif request.user.is_authenticated:
        city = City.objects.get(id=UserProfile.objects.get(user=request.user).city.id)
    else:
        city = City.objects.get(name="Gdańsk")

    latitude = city.latitude
    longitude = city.longitude
    context = {
        'city': city,
        'latitude': latitude,
        'longitude': longitude,
    }

    weather_data = get_weather(latitude, longitude)
    if weather_data:
        current_data = current_weather(weather_data)
        context.update(current_data)

        hourly_data = hourly_weather(weather_data)
        context.update(hourly_data)

        daily_data = daily_weather(weather_data)
        context.update(daily_data)

        fishing_data = fishing_parameters(weather_data)
        context.update(fishing_data)

        print(context)

        return render(request, "app/index.html", context=context)
    else:
        return HttpResponse("Error occurred" + str(weather_data))


def weather_in(request):
    if request.method == 'POST':
        city = request.POST['city']
        return index(request, city)
    else:
        return redirect('index')

