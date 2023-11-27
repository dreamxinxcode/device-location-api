from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from typing import List, Optional, Dict, Any

class Device(models.Model):
    powered_on: Optional[timezone.datetime] = models.DateTimeField(blank=True, null=True)

    @property
    def locations(self) -> List[Dict[str, Any]]:
        # Handle for devices that were never powered on.
        if not self.powered_on:
            return []
        return self.aggregated_locations()

    def aggregated_locations(self, step: int=10) -> List[Dict[str, Any]]:
        # Return a list of dictionaries containing aggregated location data.
        points = Location.objects.filter(timestamp__gt=self.powered_on).order_by('-timestamp')
        aggregated_locations = []

        for i in range(0, len(points), step):
            group = points[i:i + step]
            average_lon = sum(loc.lon for loc in group) / len(group)
            average_lat = sum(loc.lat for loc in group) / len(group)
            average_alt = sum(loc.alt for loc in group) / len(group)
            timestamp = group[-1].timestamp  # Use the timestamp of the last point

            aggregated_locations.append({
                'lon': average_lon,
                'lat': average_lat,
                'alt': average_alt,
                'timestamp': timestamp
            })

        return aggregated_locations

    def last_location(self) -> Optional[Dict[str, Any]]:
        loc = self.location_set.order_by('-timestamp').first()
        return loc if loc else None
    
    def add_location(self, lon: float, lat: float, alt: float) -> None:
        Location.objects.create(device=self, lon=lon, lat=lat, alt=alt)
        self.save()

    def power_on(self) -> None:
        self.powered_on = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f'Device: {self.id}'


class Location(models.Model):
    device: Device = models.ForeignKey('Device', on_delete=models.CASCADE)
    lon: float = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    lat: float = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    alt: float = models.FloatField(default=0)
    timestamp: timezone.datetime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.device.id} - {self.timestamp}'
