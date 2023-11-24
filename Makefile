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

cleanup:
	docker stop ${API}
	docker stop ${DB}
	docker rm ${API}
	docker rm ${DB}
	docker volume rm sw_dev_hw_project-10_pte_postgres_data
