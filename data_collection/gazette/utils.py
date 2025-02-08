import re

import dateparser
from fuzzywuzzy import process
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from gazette.database.models import QueridoDiarioSpider

MONTHS = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


def get_enabled_spiders(*, database_url, start_date=None, end_date=None):
    """Return list of all currently enabled spiders within date period.
    If start_date and/or end_date are provided, it will return only
    the enabled spiders that are within the requested date period.
    """
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = select(QueridoDiarioSpider).where(QueridoDiarioSpider.enabled.is_(True))
    if start_date is not None:
        stmt = stmt.where(QueridoDiarioSpider.date_from <= start_date)
    if end_date is not None:
        stmt = stmt.where(QueridoDiarioSpider.date_to >= end_date)

    result = session.execute(stmt)
    for spider in result.scalars():
        yield spider.spider_name


def extract_date(text):
    """Extract a date from a text. This method attempts to correct typing errors in the month.

    Args:
        text: A text containing a date with the name of the month full version (%B)
    Returns:
        The date, if match. Otherwise, returns None.
    """

    text = re.sub(" +", " ", text).strip()
    match_date = re.search(r"\d{1,2}º?(\sde)? +(\w+)(\sde)? +\d{4}", text)
    if not match_date:
        return None

    raw_date = match_date.group(0)
    raw_date = raw_date.replace("º", "").replace("°", "")
    month = match_date.group(2)
    if month.lower() not in MONTHS:
        match_month, score = process.extractOne(month, MONTHS)
        if score < 70:
            return None
        raw_date = raw_date.replace(month, match_month)

    parsed_datetime = dateparser.parse(raw_date, languages=["pt"])
    return parsed_datetime.date() if parsed_datetime else None
