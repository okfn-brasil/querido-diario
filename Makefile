setup: 
	cp .env.example .env
	docker-compose pull
	docker-compose build
	make seed
	pip3 install -r requirements.txt
	touch .git/hooks/pre-commit
	echo "make check" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

check:
	python3 -m black .

destroy:
	echo "Removing all containers...."
	docker-compose down --rmi all --volumes --remove-orphans

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
