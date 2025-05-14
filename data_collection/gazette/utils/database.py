from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from gazette.database.models import PublicEntity, Scraper


def get_enabled_spiders(*, database_url, start_date=None, end_date=None):
    """Return list of all currently enabled spiders within date period.
    If start_date and/or end_date are provided, it will return only
    the enabled spiders that are within the requested date period.
    """
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    stmt = select(Scraper).where(Scraper.ativo.is_(True))
    if start_date is not None:
        stmt = stmt.where(Scraper.data_inicial <= start_date)
    if end_date is not None:
        stmt = stmt.where(Scraper.data_final >= end_date)

    result = session.execute(stmt)
    for spider in result.scalars():
        yield spider.nome


def get_city_slug(database_url, public_entity_id):
    """Return slug related to id registered in the database"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    slug = (
        session.query(PublicEntity.slug)
        .where(PublicEntity.id.is_(public_entity_id))
        .scalar()
    )

    session.close()
    return slug
