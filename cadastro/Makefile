DOCKER_COMPOSE := docker-compose -f docker-compose.yml
DJANGO := docker-compose exec app python manage.py  

build:
		@${DOCKER_COMPOSE} build

start:
		@${DOCKER_COMPOSE} up

start-d:
		@${DOCKER_COMPOSE} up -d

stop:
		@${DOCKER_COMPOSE} down --remove-orphans

restart:
		@${DOCKER_COMPOSE} restart

migrations:
		@${DJANGO} makemigrations

migrate:
		@${DJANGO} migrate

superuser:
		@${DJANGO} createsuperuser

db: 
		@${DOCKER_COMPOSE} exec db psql -U user

logs:
		@${DOCKER_COMPOSE} logs

test:
		@${DOCKER_COMPOSE} test

collectstatic:
		@${DJANGO} collectstatic --no-input --clear
