# Contributing

*Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.*

Since Diário Oficial seeks to become a trustful source of official governmental announcements, every data source must also be trustful. A private company publishing government gazettes without official permission, for instance, is not a trustful source.

At this moment, the project aims for the 100 top Brazilian municipalities by population, collecting all the gazettes since 2015. If you want to help us reach this goal, we're tracking the progress of crawlers in [CITIES.md](CITIES.md) file. Have a look at it if you want to know where contributors are already working.

## Starting to contribute

If you have never contributed to any open source project, there are tasks just for you. They are [labeled "good first issue"](https://github.com/okfn-brasil/diario-oficial/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Before starting, drop a comment saying you plan to work on it and if you have significant questions.

Sometimes the community organizes events for solving multiple issues in a short amount of time. Especially in these cases, an issue or pull request may be considered abandoned when is waiting for the contributor but doesn't receive updates for a couple of weeks. Just let us know you need more time, so we don't end up closing it by mistake.

### Setup

Please refer to the [README file](README.md) to set up the project. Also, read the `Makefile` for understanding the available tasks and what they run.

### Writing crawlers for new municipalities

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

In order to make our life easier, the following command does the same of the previous one:

```sh
SPIDER=rs_porto_alegre make run_spider
```

## Automated code formatting

The project uses [Black](https://github.com/psf/black) as an automated tool to format and check code style. If you run `make setup` you should probably be ready to go. It will set up a pre-commit Git hook to format code that happens to be in dissonance with the code style.

Alternatively, just install Black and run it by yourself:

```sh
$ pip install black
$ black .
```

It is important to note that the CI will fail if you commit Python code that is not in accordance with Black code style.

## Guidelines to maintainers

This section is a space for project maintainers, since as code review and repository organization are part of the contribution process, all code review guidelines are of public interest to anyone in the community.

### Responsibilities of a Querido Diario maintainer:

- Respect the [code of conduct](https://github.com/okfn-brasil/querido-diario/blob/main/CODE_OF_CONDUCT.md) and ensure that anyone who may have suffered harassment has a help channel.
- Always justify a suggestion according to the practices already adopted in the project, legibility and simplicity. It is essential for a civil project to have a structure as easy as possible for beginners.
- The maintainers should **run all the spiders before merging it**.
- If a Pull Request have many commits and their messages are not clear, use the *Squash and merge* option. It is not necessary to do squash when the commits discipline is good, as an example: [Pull Request](https://github.com/okfn-brasil/querido-diario/pull/252/commits).
