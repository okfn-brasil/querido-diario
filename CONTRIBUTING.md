# Contributing

*Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.*

Since Diário Oficial seeks to become a trustful source of official governmental announcements, every data source must also be trustful. A private company publishing government gazettes without official permission, for instance, is not a trustful source.

At this moment, the project aims for the 100 top Brazilian municipalities by population, collecting all the gazettes since 2015. If you want to help us reach this goal, [an ordered list can be found on Wikipedia](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o).

We're tracking the progress of crawlers and parser in the [CITIES.md](https://github.com/okfn-brasil/diario-oficial/blob/master/CITIES.md) file. Take a look there before starting to write any source code.

## Development

If you're not familiar with [Scrapy](https://docs.scrapy.org), read the it's documentation and follow the [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) before writing any code.

To run your crawler locally, run the command bellow passing the name of the crawler you want to execute:

```sh
$ docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl <CRAWLER_NAME>"
```

### Extracting data

Use the [Scrapy shell](https://doc.scrapy.org/en/latest/intro/tutorial.html#extracting-data) to test queries on the web pages to extract data. It opens an interactive shell so you can easilly test queries to extract data:

```sh
docker-compose run --rm processing scrapy shell 'https://www.joinville.sc.gov.br/jornal/index/page/1'
```

## Automated Testing

The project is backed by a test suite, which can be run with a single command.

```sh
$ make test
```
