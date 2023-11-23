from django.db import models
from django.utils import timezone

class Device(models.Model):
    locations = models.JSONField(default=list)
    last_update = models.DateTimeField(blank=True, null=True)

    @property
    def last_location(self):
        return self.locations[-1] if self.locations else None

    def add_location(self, lon: float, lat: float, alt: float):
        new_location = {'lon': lon, 'lat': lat, 'alt': alt}

        self.locations.append(new_location)
        self.last_update = timezone.now()

        # Remove the oldest entry if the number of entries exceeds 5.
        if len(self.locations) > 5:
            self.locations.pop(0)

        self.save()

    def __str__(self) -> str:
        return f'Device: {self.id}'
