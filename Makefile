ISORT_ARGS := --combine-star --combine-as --order-by-type --thirdparty scrapy --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

SRC_DIRS := ./data_collection

check:
	python3 -m isort --check --diff $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black --check $(SRC_DIRS)
	flake8 $(SRC_DIRS)

format:
	python3 -m isort --apply $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black $(SRC_DIRS)

run_spider:
	cd $(SRC_DIRS) && scrapy crawl $(SPIDER)

sql:
	cd $(SRC_DIRS) && sqlite3 querido-diario.db

clean:
	find ./$(SRC_DIRS)/data/* -type d -exec rm -rv {} \;

shell:
	cd $(SRC_DIRS) && scrapy shell

run_spider_since:
	cd $(SRC_DIRS) && scrapy crawl -a start=$(START) $(SPIDER)

compile:
	cd data_collection; \
	pip-compile --upgrade --no-annotate --allow-unsafe --generate-hashes requirements.in; \
	pip-compile --upgrade --no-annotate --allow-unsafe --generate-hashes requirements-dev.in
