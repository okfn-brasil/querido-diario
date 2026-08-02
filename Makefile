ISORT_ARGS := --combine-star --combine-as --order-by-type --thirdparty scrapy --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

SRC_DIRS := ./querido_diario_raspadores

sync:
	uv sync --project $(SRC_DIRS) --all-groups

check:
	uv run --project $(SRC_DIRS) isort --check --diff $(ISORT_ARGS) $(SRC_DIRS)
	uv run --project $(SRC_DIRS) black --check $(SRC_DIRS)
	uv run --project $(SRC_DIRS) flake8 $(SRC_DIRS)

format:
	uv run --project $(SRC_DIRS) isort --apply $(ISORT_ARGS) $(SRC_DIRS)
	uv run --project $(SRC_DIRS) black $(SRC_DIRS)

run_spider:
	cd $(SRC_DIRS) && uv run scrapy crawl $(SPIDER)

sql:
	cd $(SRC_DIRS) && sqlite3 querido-diario.db

clean:
	find ./$(SRC_DIRS)/data/* -type d -exec rm -rv {} \;

shell:
	cd $(SRC_DIRS) && uv run scrapy shell

run_spider_since:
	cd $(SRC_DIRS) && uv run scrapy crawl -a start=$(START) $(SPIDER)

test:
	cd $(SRC_DIRS) && uv run pytest tests/ -v

lock:
	cd $(SRC_DIRS) && uv lock --upgrade

requirements:
	cd $(SRC_DIRS) && uv export --no-hashes --no-dev --no-emit-project -o requirements.txt
