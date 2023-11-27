############################
# Variables
############################
API = 'pte_api'
DB = 'pte_db'

init:
	docker-compose build 

start:
	docker-compose up -d

migrate:
	docker exec -it $(API) python manage.py migrate

createsuperuser:
	docker exec -it $(API) python manage.py createsuperuser

shell:
	docker exec -it $(API) /bin/bash

device_sim:
	docker exec -it $(API) python scripts/device_sim.py

test:
	docker exec -it $(API) python manage.py test

cleanup:
	docker stop ${API}
	docker stop ${DB}
	docker rm ${API}
	docker rm ${DB}
	docker volume rm device-location-api_pte_postgres_data
