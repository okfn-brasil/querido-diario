# Contributing

*Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.*

Since Diário Oficial seeks to become a trustful source of official governmental announcements, every data source must also be trustful. A private company publishing government gazettes without official permission, for instance, is not a trustful source.

At this moment, the project aims for the 100 top Brazilian municipalities by population, collecting all the gazettes since 2015. If you want to help us reach this goal, [an ordered list can be found on Wikipedia](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o).

We're tracking the progress of crawlers and parsers in the [CITIES.md](CITIES.md) file. Have a look at it if you want to know where contributors are already working.

## Starting to contribute

If you have never contributed to any open source project, there are tasks just for you. They are [labeled "good first issue"](https://github.com/okfn-brasil/diario-oficial/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Before starting, drop a comment saying you plan to work on it and if you have significant questions.

Sometimes the community organizes events for solving multiple issues in a short amount of time. Especially in these cases, an issue or pull request may be considered abandoned when is waiting for the contributor but doesn't receive updates for a couple of weeks. Just let us know you need more time, so we don't end up closing it by mistake.

### Option 1 - writing crawlers for new municipalities

For collecting the gazettes from the official websites, we use a crawling framework called [Scrapy](https://docs.scrapy.org). You may find its [official tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) helpful to get started with the architecture. Our project can be found in the [`processing/data_collection`](processing/data_collection) folder.

Two commands may especially be useful: `scrapy shell` and `scrapy crawl`.

Scrapy has a shell interface for experimenting with crawlers, or spiders (how prefers to call it). To see how the framework reads a webpage before writing a spider for it, try the following, where you can replace the URL for a different municipality website:

```sh
$ docker-compose run --rm processing scrapy shell http://www2.portoalegre.rs.gov.br/dopa/
```

For running an existing spider, the command receives its name (in this case, `rs_porto_alegre`):

```sh
$ docker-compose run --rm processing bash -c "cd data_collection && scrapy crawl rs_porto_alegre"
```

### Option 2 - writing new parsers for municipalities

Since the goal is to have a hundred municipalities into the system, it is reasonable to imagine a smart parser, backed by Artificial Intelligence. But before heading to a more definitive solution, at the time of this writing, we're trying to process the gazette contents using simple techniques such as regular expressions.

Won't be perfect or as generic as we would like but maybe enough to populate a database to train Machine Learning and Natural Language Processing solutions. Meaning: the code you will find - and write - in the [`processing/gazette`](processing/gazette) folder is under heavy experimentation. Doesn't need to be beautiful or scalable if it works for specific municipalities.

## Automated Testing

The project is backed by a test suite, which can be run with a single command.

```sh
$ make test
```
