# Django Device Location API

![Diagram](./docs/images/deployment.png)

## Overview

This project provides a Django-based API endpoint for managing device location data. The devices emit GPS location data at a rate of 1Hz, and this API allows clients to interact with the data in various ways.

## Getting Started

#### There is a Makefile with commands, or you can run them manually. 

```bash
# Build
make init

# Start
make start

# Migrate
make migrate

# Create superuser (optional)
make createsuperuser

# Run tests
make test

# Run server
make shell
# then
./manage.py runserver 0.0.0.0:8000

# Run device simulator (in new terminal)
make device_sim

# Clean up
make cleanup
```

## Models

The `Device` model represents a device in the field, and it has the following fields:

- `powered_on`: A DateTimeField for the last time the device was powered on.
- `locations`: A property to return aggregated GPS location data.

### Methods
- `aggregated_locations`: A method that returns aggregated location data.
- `last_location`: A property that returns the last recorded location of the device.
- `add_location(lon: float, lat: float, alt: float)`: A method to add a new location to the device, updating the `last_update` field. It also keeps the number of recorded locations within a limit (5 in this case).
- `power_on`: A method for updating the `powered_on` timestamp.

## API Views

### DeviceView ViewSet

This ViewSet provides various views for managing device location data.

#### List View

- URL: `/device/`
- Method: `GET`
- Response: Returns a list of all devices and their basic information.

#### Retrieve View

- URL: `/devices/{pk}/`
- Method: `GET`
- Response: Returns detailed information about a specific device identified by its primary key.

#### Update View

- URL: `/device/{pk}/`
- Method: `PUT`
- Request Payload: JSON data containing the new location (lon, lat, alt).
- Response: Indicates whether the update was successful.

#### Destroy View

- URL: `/device/{pk}/`
- Method: `DELETE`
- Response: Deletes the specified device and returns a success message.

#### Power-on View

- URL: `/device/123/power_on/``
- Method: `POST`
- Updates the `powered_on` field of the device.

#### Last Location View

- URL: `/device/{pk}/last_location/`
- Method: `GET`
- Response: Returns the last recorded location of the specified device.

# cURL Commands for Testing
```bash
# Create and power-on
curl -X POST http://localhost:8000/device/123/power_on/

# Add a location update
curl -X PUT -H "Content-Type: application/json" -d '{"lon": 12.34, "lat": 56.78, "alt": 100.0}' http://localhost:8000/device/123/

# Request device details
curl -X GET http://localhost:8000/device/123/

# Request all devices
curl -X GET http://localhost:8000/device/

# Get last known location of device
curl -X GET http://localhost:8000/device/123/last_location/

# Delete device
curl -X DELETE http://localhost:8000/device/123/
```

# AWS Deployment

**AWS Elastic Beanstalk:**
   - I would use AWS Elastic Beanstalk to deploy and manage a Dockerized image of the Django app.

**Amazon RDS (PostgreSQL):**
   - I would use Amazon RDS to create the PostgreSQL database.

**Elastic Load Balancer (ELB):**
   - Application Load Balancer (ALB) to distribute traffic across multiple instances of the Django app.

**Auto Scaling Group:**
   - Auto Scaling Group to adjust the number of instances based on traffic.

**Amazon CloudWatch:**
   - Set up CloudWatch alarms to monitoring and alerts.

**Logging:**
   - Send logs to Amazon CloudWatch Logs.