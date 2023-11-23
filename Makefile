############################
# Variables
############################
API = 'pte_api'

init:
	docker-compose build 

start:
	docker-compose up -d

migrate:
	docker exec -it $(API) python manage.py migrate

shell:
	docker exec -it $(API) /bin/bash

device_sim:
	docker exec -it $(API) python scripts/device_sim.py
