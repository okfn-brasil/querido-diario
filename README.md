# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the territories - in PDFs.

The goal of this project is to upgrade **Diário Oficial** to the digital age, centralizing information currently only available through separate sources.

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

## Tips and tricks

There is a make target allowing you run the scrapy shell inside the container used by the crawler:

```bash
make shell
```

## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgments

This project is maintained by Open Knowledge Foundation Brasil, thanks to the support of Digital Ocean and [hundreds of other names](https://serenata.ai/en/about/).
