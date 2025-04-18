from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from gazette.database.models import QueridoDiarioSpider


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
