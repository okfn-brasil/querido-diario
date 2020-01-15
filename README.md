# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the territories - in PDFs.

The goal of this same project is to upgrade **Diário Oficial** to the year when it gets published, making accessible information that is currently only available.

When this project was initially released, had two distinct goals: creating crawlers for governments gazettes and parsing bidding exemptions from them. Now going forward, it is limited to the first objective.

## Build and Run

If you want to understand how Diário Oficial works, you'll want to get the source, build it, and run it locally.

The only prerequisites are [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/overview/), which are the tools responsible for installing all the other dependencies.

After you cloned the repository, you may want to run the following from the source folder:

```console
$ make setup
$ docker-compose up
```

### Run Gazette Crawler

The gazettes spiders are written using Scrapy framework and must be executed with crawl command: `scrapy crawl <spider filename>`.
However, it's recommended to use the processing container for that: `docker-compose run --rm processing <command>`.
The following example is the command to run the gazette crawler for Florianópolis/SC:

```console
$ docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl sc_florianopolis"
```

## Processing pipeline

There is a very simple processing pipeline to extract some info from the gazettes files. The whole pipeline run in the containers and can be started using the `docker-compose` command shown earlier in this document. Because of the startup time for all the services and their dependencies, sometimes it is necessary restart some service individually.
This pipeline is compound by three main services:

* processing: it's the web crawler, the scrapy program. Find and download the gazettes files.
* consumer: process and extract info from the gazettes text
* cnpj-finder: using the CNPJ found by the consumer service, search for more info about it in the (Brasil.io)[https://brasil.io/home] API

When the processing service found something, it saves the files on a database, disk and publishes a message in a (Kafka)[https://kafka.apache.org/] topic. The consumer program listen to the Kafka topic waiting for new gazette files published by the processing service. Once it gets something, it extracts the CNPJ from the gazette text and update a graph database. 
The CNPJs found by the consumer service are published in another Kafka topic which is monitored by the cnpj-finder service. This service will query the Brasil.io API looking for more information about the CNPJ, specially by the entity's name. If it find something, the graph database is updated adding this additional information.

### Graph database

The current version of the graph database is *very* simple. It contains only a node for each city and CNPJ found. An edge is created between city and CNPJ nodes if the CNPJ is mentioned in the gazette text for that city.

## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgments

This project is maintained by Open Knowledge Foundation Brasil, thanks to the support of Digital Ocean and [hundreds of other names](https://serenata.ai/en/about/).
