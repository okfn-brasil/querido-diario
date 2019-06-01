setup:
	cp .env.example .env
	docker-compose pull
	docker-compose build
	make seed
	pip install pre-commit
	pre-commit install

seed:
	docker-compose up -d postgres
	docker-compose run --rm processing python3 -c 'import database; database.initialize()'
	docker-compose run --rm processing bash -c 'echo "\copy territories FROM /mnt/data/territories.csv CSV HEADER;" | psql $$DATABASE_URL'

test: unit_test
	docker-compose run --rm processing black . --check

unit_test:
	docker-compose run --rm processing pytest
