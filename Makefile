test:
	docker-compose run --rm processing python -m unittest discover

setup: configure
	docker-compose pull
	docker-compose build

configure:
	cp .env.example .env
