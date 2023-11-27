from rest_framework import serializers
from .models import Device, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'lon', 'lat', 'alt', 'timestamp']

class DeviceSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    last_location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Device
        fields = ['id', 'locations', 'powered_on', 'last_location']
        read_only_fields = ['id']