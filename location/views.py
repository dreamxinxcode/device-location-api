import logging

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

LOGGER = logging.getLogger(__name__)


# Feel free to modify this are rebuild the entire API endpoint as needed.
# Below is just some boilerplate code to help get started

class DeviceView(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        """
        Function that is called when the client wants to fetch location data
        """
        LOGGER.info(f"New GET request for device {pk}")
        return Response("To be implemented!")

    def update(self, request, pk=None):
        """
        Function that handles incoming GPS data from the device in the field.
        """
        LOGGER.info(f"New update {request} Payload: {request.data}")
        return Response("To be implemented!")
