import datetime

import click
from decouple import config
from scrapinghub import ScrapinghubClient
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from gazette.database.models import QueridoDiarioSpider
from gazette.utils import get_enabled_spiders

YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)


def _schedule_job(start_date, full, spider_name):
    client = ScrapinghubClient(config("SHUB_APIKEY"))
    project = client.get_project(config("SCRAPY_CLOUD_PROJECT_ID"))

    job_settings = {
        "FILES_STORE": config("FILES_STORE"),
        "QUERIDODIARIO_DATABASE_URL": config("QUERIDODIARIO_DATABASE_URL"),
        "AWS_ACCESS_KEY_ID": config("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": config("AWS_SECRET_ACCESS_KEY"),
        "AWS_ENDPOINT_URL": config("AWS_ENDPOINT_URL"),
        "AWS_REGION_NAME": config("AWS_REGION_NAME"),
        "SPIDERMON_DISCORD_FAKE": config("SPIDERMON_DISCORD_FAKE"),
        "SPIDERMON_DISCORD_WEBHOOK_URL": config("SPIDERMON_DISCORD_WEBHOOK_URL"),
        "ZYTE_SMARTPROXY_APIKEY": config("ZYTE_SMARTPROXY_APIKEY"),
    }

    job_args = {}
    if not full:
        job_args["start_date"] = start_date

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
    "--start_date",
    default=None,
    help="Start date (YYYY-MM-DD).",
)
@click.option(
    "--end_date",
    default=None,
    help="Start date (YYYY-MM-DD).",
)
def schedule_spider(spider_name, start_date, end_date):
    sh_client = ScrapinghubClient(config("SHUB_APIKEY"))
    project = sh_client.get_project(config("SCRAPY_CLOUD_PROJECT_ID"))

    job_settings = {
        "FILES_STORE": config("FILES_STORE"),
        "QUERIDODIARIO_DATABASE_URL": config("QUERIDODIARIO_DATABASE_URL"),
        "AWS_ACCESS_KEY_ID": config("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": config("AWS_SECRET_ACCESS_KEY"),
        "AWS_ENDPOINT_URL": config("AWS_ENDPOINT_URL"),
        "AWS_REGION_NAME": config("AWS_REGION_NAME"),
        "SPIDERMON_DISCORD_FAKE": config("SPIDERMON_DISCORD_FAKE"),
        "SPIDERMON_DISCORD_WEBHOOK_URL": config("SPIDERMON_DISCORD_WEBHOOK_URL"),
        "ZYTE_SMARTPROXY_APIKEY": config("ZYTE_SMARTPROXY_APIKEY"),
    }

    job_args = {}
    if start_date:
        job_args["start_date"] = start_date
    if end_date:
        job_args["end_date"] = end_date

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
    "--start_date",
    default=YESTERDAY.strftime("%Y-%m-%d"),
    help="Start date that we want to scrape.",
)
@click.option(
    "-f",
    "--full",
    default=False,
    is_flag=True,
    help="If we want to execute a full crawl (all available dates). "
    "When this option is set to true --start_date option is ignored.",
)
@click.argument("spider_name")
def schedule_job(start_date, full, spider_name):
    _schedule_job(start_date, full, spider_name)


@cli.command()
def schedule_enabled_spiders():
    for spider_name in get_enabled_spiders(
        database_url=config("QUERIDODIARIO_DATABASE_URL"), start_date=YESTERDAY
    ):
        _schedule_job(start_date=YESTERDAY, full=False, spider_name=spider_name)


@cli.command()
def last_month_schedule_enabled_spiders():
    # Sometimes the online gazette is not published in the websites in the same
    # day as the physical one (sometimes it take more than two days and other weeks)
    # so running this command will ensure that we get the data of the latest month
    start_date = datetime.date.today() - datetime.timedelta(days=31)
    for spider_name in get_enabled_spiders(
        database_url=config("QUERIDODIARIO_DATABASE_URL"), start_date=start_date
    ):
        _schedule_job(start_date=start_date, full=False, spider_name=spider_name)


@click.option(
    "--start_date",
    help="Start date that we want to scrape all enabled spiders.",
)
@cli.command()
def schedule_all_spiders_by_date(start_date):
    for spider_name in get_enabled_spiders(
        database_url=config("QUERIDODIARIO_DATABASE_URL"), start_date=start_date
    ):
        _schedule_job(start_date, full=False, spider_name=spider_name)


if __name__ == "__main__":
    cli()
