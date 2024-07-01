import requests

from rest_framework.views import View
from django.http import JsonResponse
from django.conf import settings

def get_location(ip="129.205.113.176"):
    url = f'https://geo.ipify.org/api/v2/country,city?apiKey={settings.GEO_IPY_KEY}&ipAddress={ip}'
    response = requests.get(url)
    data = response.json()
    print(data.get('location'))
    l = data.get('location')

    return l["city"]

# Function to fetch temperature using OpenWeatherMap API
def get_temperature(city):
    print(city, "CITY")
    if city:

       url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?q=new york&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    print(data)
    temperature = data['main']['temp']
    return temperature

class Index(View):
    def get(self, request):
        query = request.GET.get('visitor_name', 'Guest')
        user_ip = request.META.get('REMOTE_ADDR', '')
        
        location = get_location(user_ip)
        print(location)
        temperature = get_temperature(location)
        
        res = {
            "client_ip": user_ip,
            "location": location,
            "greeting": f"Hello, {query}! The temperature is {temperature} degrees Celsius in {location}."
        }
        
        return JsonResponse(res)
