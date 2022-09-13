from django.shortcuts import render, get_object_or_404, redirect
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages
from .models import City

def index(request):
    API_KEY = config("API_KEY")
    city = "Erzurum"
    u_city = request.POST.get("name")
    
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        print(response.ok)
        
        if response.ok:
            content = response.json()
            r_city = content["name"]
            if City.objects.filter(name=r_city):
                messages.warning(request, "City already exists!")
            else:
                City.objects.create(name=r_city)
            
        else:
            messages.warning(request, "There is no city")
    
    
    city_data = []
    cities = City.objects.all()
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data = {
                "city" : city,
                "temp" : content["main"]["temp"],
                "icon" : content["weather"][0]["icon"],
                "desc" : content["weather"][0]["description"]
        }
        city_data.append(data)

    context = {
        "city_data" : city_data
    }
    
    return render(request, 'weatherapp/index.html', context)




def delete_city(request, id):
    # city = City.objects.get(id=id)
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.warning(request, "City deleted.")
    return redirect("home")



