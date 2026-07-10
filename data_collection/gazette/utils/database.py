from decouple import config
from scrapy import spiderloader
from scrapy.utils import project
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from gazette.database.models import QueridoDiarioSpider
from gazette.utils.api_client import QueridoDiarioAPIClient


def generate_territory_spider_map():
    """Build the (spider_name, territory_id, date_from) mapping from the
    spider classes available in the project."""
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]

    mapping = []
    for spider_class in classes:
        spider_name = getattr(spider_class, "name", None)
        territory_id = getattr(spider_class, "TERRITORY_ID", None)
        date_from = getattr(spider_class, "start_date", None)
        if all((spider_name, territory_id, date_from)):
            mapping.append((spider_name, territory_id, date_from))
    return mapping


def get_enabled_spiders(
    *, database_url=None, start_date=None, end_date=None, api_url=None, api_key=None
):
    """Return list of all currently enabled spiders within date period.
    If start_date and/or end_date are provided, it will return only
    the enabled spiders that are within the requested date period.

    When QUERIDODIARIO_API_URL is configured (argument or environment
    variable), the list is fetched from the Querido Diário API. Otherwise
    it falls back to direct database access through database_url (local
    development compatibility).
    """
    api_url = api_url or config("QUERIDODIARIO_API_URL", default="")
    if api_url:
        api_key = api_key or config("QUERIDODIARIO_API_KEY", default="")
        client = QueridoDiarioAPIClient(api_url, api_key)
        yield from client.get_enabled_spiders(start_date=start_date, end_date=end_date)
        return

    if not database_url:
        raise RuntimeError(
            "Neither QUERIDODIARIO_API_URL nor QUERIDODIARIO_DATABASE_URL is set. "
            "Configure one of them to fetch enabled spiders."
        )
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
