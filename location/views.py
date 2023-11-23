import logging

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Device
from.serializers import DeviceSerializer

LOGGER = logging.getLogger(__name__)


# Feel free to modify this are rebuild the entire API endpoint as needed.
# Below is just some boilerplate code to help get started

class DeviceView(viewsets.ViewSet):

    def retrieve(self, request, pk: int=None):
        device = get_object_or_404(Device, id=pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk: int=None):
        device, _ = Device.objects.get_or_create(id=pk)
        device.add_location(**request.data)
        LOGGER.info(f"New update {request} Payload: {request.data}")
        return Response("Update successful!", status=status.HTTP_200_OK)