# Diário Oficial

## Setup

1. Install [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/overview/).

```
$ cp .env.sample .env
$ docker-compose run data_collection \
    scrapy crawl rs_porto_alegre
```
