from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Device
from .serializers import DeviceSerializer


class DeviceView(viewsets.ViewSet):
    serializer_class = DeviceSerializer
    
    def list(self, request) -> Response:
        try:
            queryset = Device.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk: int=None) -> Response:
        try:
            device = get_object_or_404(Device, id=pk)
            serializer = self.serializer_class(device)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response("Device not found", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk: int=None) -> Response:
        try:
            device, _ = Device.objects.get_or_create(id=pk)
            device.add_location(**request.data)
            return Response("Update successful!", status=status.HTTP_200_OK)
        except Exception:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None) -> Response:
        try:
            device = get_object_or_404(Device, id=pk)
            device.delete()
            return Response("Device deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET'])
    def last_location(self, request, pk: int=None) -> Response:
        try:
            device = get_object_or_404(Device, id=pk)
            serializer = self.serializer_class(device)
            return Response(serializer.data.get('last_location') or "No location data available for this device.", status=status.HTTP_200_OK)
        except Exception:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def power_on(self, request, pk: int=None) -> Response:
        try:
            device, _ = Device.objects.get_or_create(id=pk)
            device.power_on()
            return Response("Power-on received successfully.", status=status.HTTP_200_OK)
        except Exception:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)