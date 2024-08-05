import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
from .models import Country, City, UserProfile

from .forms import LoginForm, UserRegisterForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid username or password')
                return render(request, 'users/login.html', context={'form': form})


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', context={'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form['country'] is not None:
            cities_list = City.objects.filter(country=Country.objects.get(name=form['country'].value()).id)
        #     form.fields['city'].queryset = cities_list
        #     print(form.fields['city'].queryset)



        if form.is_valid():
            cities_list = fetch_cities(form['country'].value())
            print(f'{request.POST['city'] =}')
            if request.POST['city'] in cities_list:
                print("IN THE LIST LESGO")
            else:
                print("city list")

            user = form.save()
            userprofile = UserProfile.objects.create(user=user, city=City.objects.get(name=request.POST['city']))
            userprofile.save()
            login(request, user)
            return redirect('/')
        else:
            # print(form['city'].value())
            # print(form.errors)
            return render(request, 'users/register.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def cities(request):
    if request.method == 'POST':
        country = request.POST['country']
        cities_list = sorted(fetch_cities(country))
        # print("IN CITIES", cities_list)
        return HttpResponse(json.dumps(cities_list), content_type="application/json")


def index(request):
    return redirect('login')


# Utility function to fill local database with countries
def populate_countries() -> None:
    countries_list = fetch_countries()
    for country in countries_list:
        Country.objects.create(name=country)


# Utility function to get all the countries using api
def fetch_countries() -> list[str]:
    response = requests.get('https://restcountries.com/v3.1/all?fields=name')
    raw = response.json()
    countries = []
    for country in raw:
        countries.append(country['name']['common'])
    return countries


# Utility function to fill local database with cities
def populate_cities() -> None:
    countries_list = Country.objects.all()
    for cntry in countries_list:
        for city in fetch_cities(cntry):
            print(cntry, city)
            City.objects.create(name=city, country=cntry)


def clear_unused_countries() -> None:
    cities_list = City.objects.all()
    for city in cities_list:
        if str(city.name) == str(city.country) and len(City.objects.filter(country=city.country)) == 1:
            print(city)


# Utility function to get all the cities within the country using api
def fetch_cities(country: str) -> list[str]:
    try:
        print(country)
        cities_list = City.objects.filter(country=Country.objects.get(name=country).id)
        city_names = [city.name for city in cities_list]
        # print(city_names)
        return city_names
    except Exception as e:
        temp = []
        temp.append(country)
        return temp
