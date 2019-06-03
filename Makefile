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
