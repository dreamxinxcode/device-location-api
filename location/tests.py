from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Device

class DeviceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_devices(self):
        response = self.client.get('/device/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_device(self):
        device = Device.objects.create()
        response = self.client.get(f'/device/{device.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_device(self):
        data = {'lat': 12.345, 'lon': 45.678, 'alt': 100}
        response = self.client.put('/device/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Update successful!')

    def test_destroy_device(self):
        device = Device.objects.create()
        response = self.client.delete(f'/device/{device.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())

    def test_last_location(self):
        device = Device.objects.create()
        response = self.client.get(f'/device/{device.id}/last_location/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'No location data available for this device.')