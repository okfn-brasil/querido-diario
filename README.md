# Diário Oficial

**Diário Oficial** is the Brazilian government gazette, one of the best places to know the latest actions of the public administration, with distinct publications in the federal, state and municipal levels.

Even with recurrent efforts of enforcing the [Freedom of Information legislation](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) across the country, official communication remains - in most of the territories - in PDFs.

The goal of this project is to upgrade **Diário Oficial** to the digital age, centralizing information currently only available through separate sources.

When this project was initially released, had two distinct goals: creating crawlers for governments gazettes and parsing bidding exemptions from them. Now going forward, it is limited to the first objective.

Table of Contents
=================
  * [Development environment](#development-environment)
     * [Run Gazette Crawler](#run-gazette-crawler)
  * [Contributing](#contributing)
  * [Acknowledgments](#acknowledgments)

## Development environment

The best way to understand how **Querido Diário** works, is getting the source
and run it locally. All crawlers are developed using [Scrapy](https://scrapy.org)
framework. They provide a [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
so you can learn to use it.

If you are in a Linux-like environment, the following commands will create a new
[virtual environment](https://docs.python.org/3/library/venv.html) - that will keep
everything isolated from your system - activate it and install all libraries needed
to start running and developing new spiders.

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ cd processing/data_collection/
$ pip install -r requirements.txt
```

### Run Gazette Crawler

After configuring your environment, you will be able to execute and develop new spiders.
Following we list some helpful commands.

Get list of all available spiders:

```console
$ scrapy list
```

Execute spider with name `spider_name`:

```console
$ scrapy crawl spider_name
```

You can limit the gazettes you want to download passing `start_date` as argument with `YYYY-MM-DD` format. The
following command will download only gazettes which date is greater than 01/Sep/2020:

```console
$ scrapy crawl sc_florianopolis -a start_date=2020-09-01
```

## Contributing

If you are interested in fixing issues and contributing directly to the code base, please see the document [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgments

This project is maintained by Open Knowledge Foundation Brasil, thanks to the support of Digital Ocean and [hundreds of other names](https://serenata.ai/en/about/).
