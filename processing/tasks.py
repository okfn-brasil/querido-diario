from celery import Celery
from celery.schedules import crontab
from decouple import config

from database.models import BiddingExemption, Gazette
from gazette.data.bidding_exemption_parsing import BiddingExemptionParsing
from gazette.data.row_update import RowUpdate
from gazette.data.section_parsing import SectionParsing

app = Celery('tasks', backend=config('REDIS_URL'), broker=config('RABBITMQ_URL'))
PARSING_FREQUENCY = config('PARSING_FREQUENCY_IN_SECONDS', cast=int)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PARSING_FREQUENCY, parse_sections.s())


@app.task
def parse_sections():
    row_update = RowUpdate(Gazette)
    row_update(SectionParsing)
    parse_bidding_exemptions.delay()


@app.task
def parse_bidding_exemptions():
    row_update = RowUpdate(BiddingExemption)
    row_update(BiddingExemptionParsing)
