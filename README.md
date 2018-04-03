# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels of the country.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the municipalities - in PDFs.

The goal of this same project is to upgrade **Diário Oficial** to the year when it gets published, making accessible information that was currently only available.

**At the current state, there isn't much to see or download. Come back in a few weeks. :)**

*Unless you are a software developer and want to contribute even in this chaotic starting moment. In this case, make yourself at home and start downloading [Docker](https://www.docker.com) and with [Docker Compose](https://docs.docker.com/compose/overview/).*

## Setup

```
$ cp .env.sample .env
$ docker-compose run data_collection \
    scrapy crawl rs_porto_alegre
```

## Running the test suite

```
$ docker-compose run --rm processing \
    python -m unittest discover
```