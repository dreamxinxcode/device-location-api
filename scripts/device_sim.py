#!/usr/bin/env python3

import logging
import json
import time
import random
import requests

import geopy
import geopy.distance

logging.basicConfig(level=logging.INFO)


def new_point(origin, angle, distance=10):
    """
    Function that returns a new WP based on the distance(m) and origin

    Args:
      origin (geopy.Point): Coordinates that will be the base of the new Waypoint
      angle (int): Angle or bearing of new Waypoint in Meters
      distance (int): Distance in meters from origin

    NOTE: This func does select a random angle/bearing. It also has
    a percentage where the bearing will be the same to simulate
    device moving in straight line (30% chance). At time the device
    may pause in the same location too (10% chance).
    """
    if random.random() < 0.70:
        # we compute a new angle
        angle = random.randint(0, 90)

    if random.random() < 0.10:
        # assume the device is paused in the same spot
        return origin, angle

    return geopy.distance.distance(meters=distance).destination(origin, bearing=angle), angle


def send_to_api(point):
    p = {
        'lon': point.longitude,
        'lat': point.latitude,
        'alt': point.altitude,
    }

    logging.info(f'Sending coords to backend: {p}')
    r = requests.put('http://127.0.0.1:8000/device/123/', json=p)
    if not r.ok:
        logging.error(f'Unable to send to API, status code: {r.status_code}, error: {r.text}')


def device_sim(origin):
    last_angle = 0

    while True:
        new_wpt, last_angle = new_point(origin, last_angle)

        logging.debug(f'Emitting new position {new_wpt.format_decimal()}')
        send_to_api(new_wpt)

        origin = new_wpt
        time.sleep(1)


if __name__ == '__main__':
    logging.info('Starting device simulation at 1Hz output')
    device_sim(geopy.Point(43.642566, -79.387057))
