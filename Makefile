ENV_FILE := .env

setup:
	cp .env.example $(ENV_FILE)
	docker-compose pull
	docker-compose build
	pip3 install -r requirements.txt
	touch .git/hooks/pre-commit
	echo "make check" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

check:
	python3 -m black .

ISORT_ARGS := --recursive --combine-star --combine-as --order-by-type --thirdparty scrapy --builtin dateparser --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

SRC_DIRS := ./processing

check:
	python3 -m isort --check --diff $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black --check $(SRC_DIRS)

format:
	python3 -m isort --apply $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black $(SRC_DIRS)

destroy:
	echo "Removing all containers...."
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose rm -v -s -f
	rm -f $(ENV_FILE)

test:
	black . --check

run_spider:
	docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl $(SPIDER)"

sql:
	docker-compose run --rm processing sqlite3 data_collection/querido-diario.db

clean:
	find ./data/* -type d -exec rm -rv {} \;

build:
	docker build -t $(NAMESPACE)/diario-oficial:$(shell date --rfc-3339=date --utc) -t $(NAMESPACE)/diario-oficial:latest processing

publish:
	docker push $(NAMESPACE)/diario-oficial:$(shell date --rfc-3339=date --utc)
	docker push $(NAMESPACE)/diario-oficial:latest

shell:
	docker-compose run --rm processing bash -c "cd data_collection && scrapy shell"

run_spider_since:
	docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl -a start_date=$(START_DATE) $(SPIDER)"
