test:
	docker-compose run --rm processing python -m unittest discover
	docker-compose run --rm processing bash -c "cd data_collection && scrapy check"

setup: configure
	docker-compose pull
	docker-compose build

configure:
	cp .env.example .env
