from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.core.cache import cache
from .models import Shipment

class ShipmentAPITestCase(APITestCase):

    def setUp(self):
        # Create test shipment data
        Shipment.objects.create(
            id=1,
            tracking_number="TN12345682",
            carrier="GLS",
            sender_address="Street 5, 70173 Stuttgart, Germany",
            receiver_address="Street 15, 1050 Copenhagen, Denmark",
            article_name="Smartphone",
            article_quantity=1,
            article_price="500.00",
            SKU="SP901",
            status="scanned"
        )

    @patch('requests.get')
    def test_shipment_detail_no_cache(self, mock_get):
        # Mock weather API response
        mock_weather_data = {
            'weather': [{'description': 'clear sky'}],
            'main': {'temp': 15}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_weather_data

        # First request should fetch from the API (no cache hit)
        response = self.client.get('/shipments/GLS/TN12345682/')
        
        # Assert API response and cache miss (calls external weather API)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('weather', response.json())
        self.assertEqual(response.json()['weather']['main']['temp'], 15)
        mock_get.assert_called_once()  # External API call happens on the first request

    @patch('requests.get')
    def test_shipment_detail_with_cache(self, mock_get):
        # Mock weather API response
        mock_weather_data = {
            'weather': [{'description': 'clear sky'}],
            'main': {'temp': 15}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_weather_data

        # First request (fetch from API and set cache)
        response = self.client.get('/shipments/GLS/TN12345682/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Clear the mock call count and simulate the second request (should hit the cache)
        mock_get.reset_mock()
        
        # Second request (should fetch from cache, no external API call)
        response = self.client.get('/shipments/GLS/TN12345682/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('weather', response.json())
        self.assertEqual(response.json()['weather']['main']['temp'], 15)
        mock_get.assert_not_called()  # Cache hit, no external API call

    @patch('requests.get')
    def test_shipment_detail_weather_null(self, mock_get):
        # Simulate external API failure (weather API returns 404)
        mock_get.return_value.status_code = 404

        # Make a request to the API
        response = self.client.get('/shipments/GLS/TN12345682/')

        # Assert that the weather data is null in the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json()['weather'])
        mock_get.assert_called_once()  # External API call happens but fails

    def test_shipment_not_found(self):
        # Request for a shipment that does not exist
        response = self.client.get('/shipments/GLS/TN00000000/')
        
        # Assert 404 not found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Not found')

    def tearDown(self):
        # Clear the cache after tests
        cache.clear()
