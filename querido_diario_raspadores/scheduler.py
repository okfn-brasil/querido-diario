import datetime

import click
from decouple import config
from scrapinghub import ScrapinghubClient
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from gazette.database.models import QueridoDiarioSpider
from gazette.utils.database import get_enabled_spiders

YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)


def _job_settings():
    return {
        "FILES_STORE": config("FILES_STORE"),
        "FILES_STORE_SECONDARY": config("FILES_STORE_SECONDARY", default=""),
        # Gazettes are persisted through the API when QUERIDODIARIO_API_URL
        # is set. QUERIDODIARIO_DATABASE_URL is kept only while job_stats
        # (phase 2) has not migrated to the API.
        "QUERIDODIARIO_API_URL": config("QUERIDODIARIO_API_URL", default=""),
        "QUERIDODIARIO_API_KEY": config("QUERIDODIARIO_API_KEY", default=""),
        "QUERIDODIARIO_DATABASE_URL": config("QUERIDODIARIO_DATABASE_URL", default=""),
        "AWS_ACCESS_KEY_ID": config("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": config("AWS_SECRET_ACCESS_KEY"),
        "AWS_ENDPOINT_URL": config("AWS_ENDPOINT_URL"),
        "AWS_REGION_NAME": config("AWS_REGION_NAME"),
        "SPIDERMON_DISCORD_FAKE": config("SPIDERMON_DISCORD_FAKE"),
        "SPIDERMON_DISCORD_WEBHOOK_URL": config("SPIDERMON_DISCORD_WEBHOOK_URL"),
        "ZYTE_SMARTPROXY_APIKEY": config("ZYTE_SMARTPROXY_APIKEY"),
    }


def _get_enabled_spiders(start_date=None, end_date=None):
    return get_enabled_spiders(
        database_url=config("QUERIDODIARIO_DATABASE_URL", default=None),
        api_url=config("QUERIDODIARIO_API_URL", default=""),
        api_key=config("QUERIDODIARIO_API_KEY", default=""),
        start_date=start_date,
        end_date=end_date,
    )


def _get_project():
    client = ScrapinghubClient(config("SHUB_APIKEY"))
    return client.get_project(config("SCRAPY_CLOUD_PROJECT_ID"))


def _schedule_job(start, full, spider_name, project=None, end=None):
    project = project or _get_project()

    job_settings = _job_settings()

    job_args = {}
    if not full:
        job_args["start"] = start
        if end:
            job_args["end"] = end

    spider = project.spiders.get(spider_name)
    spider.jobs.run(
        job_settings=job_settings,
        job_args=job_args,
    )


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--spider_name",
    required=True,
    help="Spider name to execute.",
)
@click.option(
    "--start",
    default=None,
    help="Start date (YYYY-MM-DD).",
)
@click.option(
    "--end",
    default=None,
    help="Start date (YYYY-MM-DD).",
)
def schedule_spider(spider_name, start, end):
    sh_client = ScrapinghubClient(config("SHUB_APIKEY"))
    project = sh_client.get_project(config("SCRAPY_CLOUD_PROJECT_ID"))

    job_settings = _job_settings()

    job_args = {}
    if start:
        job_args["start"] = start
    if end:
        job_args["end"] = end

    spider = project.spiders.get(spider_name)
    spider.jobs.run(
        job_settings=job_settings,
        job_args=job_args,
    )


@cli.command()
@click.option(
    "--spider_name",
    required=True,
    help="Spider name",
)
def enable_spider(spider_name):
    engine = create_engine(config("QUERIDODIARIO_DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = (
        update(QueridoDiarioSpider)
        .where(QueridoDiarioSpider.spider_name == spider_name)
        .values(enabled=True)
    )

    session.execute(stmt)
    session.commit()


@cli.command()
@click.option(
    "--spider_name",
    required=True,
    help="Spider name",
)
def disable_spider(spider_name):
    engine = create_engine(config("QUERIDODIARIO_DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = (
        update(QueridoDiarioSpider)
        .where(QueridoDiarioSpider.spider_name == spider_name)
        .values(enabled=False)
    )

    session.execute(stmt)
    session.commit()


@cli.command()
@click.option(
    "--start",
    default=YESTERDAY.strftime("%Y-%m-%d"),
    help="Start date that we want to scrape.",
)
@click.option(
    "-f",
    "--full",
    default=False,
    is_flag=True,
    help="If we want to execute a full crawl (all available dates). "
    "When this option is set to true --start option is ignored.",
)
@click.argument("spider_name")
def schedule_job(start, full, spider_name):
    _schedule_job(start, full, spider_name)


@cli.command()
def schedule_enabled_spiders():
    project = _get_project()
    for spider_name in _get_enabled_spiders(start_date=YESTERDAY):
        _schedule_job(
            start=YESTERDAY,
            full=False,
            spider_name=spider_name,
            project=project,
        )


@cli.command()
@click.option(
    "--start",
    default=None,
    help="Start date (YYYY-MM-DD). Defaults to 31 days ago.",
)
@click.option(
    "--end",
    default=None,
    help="End date (YYYY-MM-DD). Defaults to no end bound (today).",
)
def last_month_schedule_enabled_spiders(start, end):
    # Sometimes the online gazette is not published in the websites in the same
    # day as the physical one (sometimes it take more than two days and other weeks)
    # so running this command with no arguments will ensure that we get the data
    # of the latest month. --start/--end allow overriding the window to
    # (re)schedule enabled spiders over any custom date range instead.
    if start is None:
        start = datetime.date.today() - datetime.timedelta(days=31)
    project = _get_project()
    for spider_name in _get_enabled_spiders(start_date=start, end_date=end):
        _schedule_job(
            start=start, end=end, full=False, spider_name=spider_name, project=project
        )


@click.option(
    "--start",
    help="Start date that we want to scrape all enabled spiders.",
)
@cli.command()
def schedule_all_spiders_by_date(start):
    project = _get_project()
    for spider_name in _get_enabled_spiders(start_date=start):
        _schedule_job(start=start, full=False, spider_name=spider_name, project=project)


if __name__ == "__main__":
    cli()
