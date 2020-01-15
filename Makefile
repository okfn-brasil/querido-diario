setup:
	cp .env.example .env
	docker-compose pull
	docker-compose build
	make seed
	@if [ -z $$VIRTUAL_ENV ]; then \
		pip install --user pre-commit; \
	else \
		pip install pre-commit; \
	fi
	pre-commit install

seed:
	docker-compose up -d postgres
	docker-compose run --rm processing bash seed.sh

test:
	docker-compose run --rm processing black . --check

run_spider:
	docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl $(SPIDER)"

sql:
	docker-compose run --rm postgres psql --username gazette -h postgres -W

clean:
	find data/full/ -delete

up:
	docker-compose up -d

down:
	docker-compose down

restart: down up

ps:
	docker-compose ps

consumer-start:
	docker-compose start consumer

consumer-stop:
	docker-compose stop consumer

restart-consumer: consumer-stop consumer-start

cnpj-finder-start:
	docker-compose start cnpj-finder

cnpj-finder-stop:
	docker-compose stop cnpj-finder

restart-cnpj-finder: cnpj-finder-stop cnpj-finder-start
