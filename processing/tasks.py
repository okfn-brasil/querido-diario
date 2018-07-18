import datetime as dt
import pkgutil
import subprocess

from celery import Celery
from celery.schedules import crontab
from decouple import config

from data_collection.gazette import spiders
from database.models import BiddingExemption, Gazette
from gazette.data.bidding_exemption_parsing import BiddingExemptionParsing
from gazette.data.row_update import RowUpdate
from gazette.data.section_parsing import SectionParsing

app = Celery("tasks", backend=config("REDIS_URL"), broker=config("RABBITMQ_URL"))
PARSING_FREQUENCY = config("PARSING_FREQUENCY_IN_SECONDS", cast=int)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PARSING_FREQUENCY, parse_sections.s())
    sender.add_periodic_task(
        crontab(hour=13),
        run_spiders.s(["go_goiania", "rs_porto_alegre"], timerange="past_week"),
    )


@app.task
def parse_sections():
    row_update = RowUpdate(Gazette)
    row_update(SectionParsing)
    parse_bidding_exemptions.delay()


@app.task
def parse_bidding_exemptions():
    row_update = RowUpdate(BiddingExemption)
    row_update(BiddingExemptionParsing)


@app.task
def run_spider(spider_name, timerange=None):
    run_spiders([spider_name], timerange)


@app.task
def run_spiders(spiders=None, timerange=None):
    command_params = []
    if not spiders:
        spiders = all_spiders()
    if timerange == "past_week":
        start_date = str((dt.datetime.today() - dt.timedelta(days=7)).date())
        command_params = ["-a", "start_date=" + start_date]
    elif timerange is not None:
        raise ValueError(
            "timerange not supported."
            'The only possible values are "past_week" and None.'
        )

    for spider_name in spiders:
        command = ["scrapy", "crawl", spider_name] + command_params
        subprocess.Popen(command, cwd="data_collection")


def all_spiders():
    names = []
    for info in pkgutil.walk_packages(path=spiders.__path__):
        if info.name != "base":
            names.append(info.name)
    return names
