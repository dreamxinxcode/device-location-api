import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Device
from.serializers import DeviceSerializer

LOGGER = logging.getLogger(__name__)

class DeviceView(viewsets.ViewSet):
    serializer = DeviceSerializer
    
    def list(self, request):
        try:
            queryset = Device.objects.all()
            serializer = self.serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            LOGGER.error(f"Error in listing devices: {e}")
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk: int=None):
        try:
            device = get_object_or_404(Device, id=pk)
            serializer = self.serializer(device)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            LOGGER.error(f"Error in retrieving device: {e}")
            return Response("Device not found", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk: int=None):
        try:
            device, _ = Device.objects.get_or_create(id=pk)
            device.add_location(**request.data)
            LOGGER.info(f"New update {request} Payload: {request.data}")
            return Response("Update successful!", status=status.HTTP_200_OK)
        except Exception as e:
            LOGGER.error(f"Error in updating device: {e}")
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        try:
            device = get_object_or_404(Device, id=pk)
            device.delete()
            return Response("Device deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            LOGGER.error(f"Error in deleting device: {e}")
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET'])
    def last_location(self, request, pk: int=None):
        try:
            device = get_object_or_404(Device, id=pk)
            serializer = self.serializer(device)
            last_location = serializer.data.get('last_location')
            return Response(last_location or "No location data available for this device.", status=status.HTTP_200_OK)
        except Exception as e:
            LOGGER.error(f"Error in retrieving last location: {e}")
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
