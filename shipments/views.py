from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shipment
from rest_framework import status
from .serializers import ShipmentSerializer
import requests
from django.core.cache import cache
import environ

env = environ.Env()
environ.Env.read_env()

WEATHER_API_KEY = env('WEATHER_API_KEY')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to get the weather information
def get_weather_data(zip_code):
    cache_key = f'weather_{zip_code}'
    weather_data = cache.get(cache_key)

    if weather_data:
        return weather_data

    print(f"Fetching weather data for {zip_code}")
    # If not in cache, fetch from API
    params = {
        'zip': zip_code,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(WEATHER_API_URL, params=params)
    print(response, zip_code)
    if response.status_code == 200:
        weather_data = response.json()
        print(weather_data)
        cache.set(cache_key, weather_data, timeout=2*60*60)  # Cache for 2 hours
        return weather_data
    return None

# API view to get shipments by carrier and tracking number
@api_view(['GET'])
def shipment_detail(request, carrier, tracking_number):
    # Fetch all shipments with the given carrier and tracking_number
    shipments = Shipment.objects.filter(carrier=carrier, tracking_number=tracking_number)
    
    if not shipments:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the queryset
    serializer = ShipmentSerializer(shipments, many=True)

    # Extract ZIP code from receiver's address of the first shipment (assuming similar address format)
    receiver_address = shipments[0].receiver_address
    zip_code = receiver_address.split(",")[-2].split(' ')[1]  # Extracting ZIP code

    # Get weather data for the receiver's location
    weather_data = get_weather_data(zip_code)
    
    response_data = {
        'shipments': serializer.data,
        'weather': weather_data
    }
    
    return Response(response_data)
