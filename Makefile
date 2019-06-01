setup:
	cp .env.example .env
	docker-compose pull
	docker-compose build
	make seed
	pip install pre-commit
	pre-commit install

seed:
	docker-compose up -d postgres
	docker-compose run --rm processing bash seed.sh

test:
	docker-compose run --rm processing black . --check
