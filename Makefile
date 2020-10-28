ENV_FILE := .env
ISORT_ARGS := --recursive --combine-star --combine-as --order-by-type --thirdparty scrapy --builtin dateparser --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88
SRC_DIRS := ./data_collection

check:
	python3 -m isort --check --diff $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black --check $(SRC_DIRS)

format:
	python3 -m isort --apply $(ISORT_ARGS) $(SRC_DIRS)
	python3 -m black $(SRC_DIRS)

run_spider:
	cd data_collection && scrapy crawl $(SPIDER)

sql:
	sqlite3 data_collection/querido-diario.db

clean:
	find ./data_collection/data/* -type d -exec rm -rv {} \;

shell:
	cd data_collection && scrapy shell

run_spider_since:
	cd data_collection && scrapy crawl -a start_date=$(START_DATE) $(SPIDER)
