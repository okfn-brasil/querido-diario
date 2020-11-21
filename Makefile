ISORT_ARGS := --recursive --combine-star --combine-as --order-by-type --thirdparty scrapy --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

SRC_DIRS := ./data_collection

check:

format:

run_spider:
	cd $(SRC_DIRS) && scrapy crawl $(SPIDER)

sql:
	cd $(SRC_DIRS) && sqlite3 querido-diario.db

clean:
	find ./$(SRC_DIRS)/data/* -type d -exec rm -rv {} \;

shell:
	cd $(SRC_DIRS) && scrapy shell

run_spider_since:
	cd $(SRC_DIRS) && scrapy crawl -a start_date=$(START_DATE) $(SPIDER)
