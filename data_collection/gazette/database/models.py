import csv
import datetime as dt
import logging

import pkg_resources
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DeclarativeBase = declarative_base()

logger = logging.getLogger(__name__)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


def load_territories(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Territory).count() > 0:
        return

    logger.info("Populating 'territories' table - Please wait!")
    territories_file = pkg_resources.resource_filename(
        "gazette", "resources/territories.csv"
    )
    with open(territories_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        territories = []
        for row in reader:
            territories.append(Territory(**row))
        session.bulk_save_objects(territories)
        session.commit()
    logger.info("Populating 'territories' table - Done!")


def load_spiders(engine, territory_spider_map):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(QueridoDiarioSpider).count() > 0:
        return

    logger.info("Populating 'querido_diario_spider' table - Please wait!")

    spiders = []
    territory_ids = set()
    for info in territory_spider_map:
        spider_name, territory_id, date_from = info
        spiders.append(
            QueridoDiarioSpider(spider_name=spider_name, date_from=date_from)
        )
        territory_ids.add(territory_id)

    session.add_all(spiders)
    session.commit()

    spiders = (
        session.query(QueridoDiarioSpider)
        .filter(
            QueridoDiarioSpider.spider_name.in_(set(s[0] for s in territory_spider_map))
        )
        .all()
    )
    spider_map = {spider.spider_name: spider for spider in spiders}

    territories = session.query(Territory).filter(Territory.id.in_(territory_ids)).all()
    territory_map = {t.id: t for t in territories}

    for info in territory_spider_map:
        spider_name, territory_id, _ = info
        spider = spider_map.get(spider_name)
        territory = territory_map.get(territory_id)
        if spider is not None and territory is not None:
            spider.territories.append(territory)

    session.commit()
    logger.info("Populating 'querido_diario_spider' table - Done!")


def initialize_database(database_url, territory_spider_map):
    engine = create_engine(database_url)
    create_tables(engine)
    load_territories(engine)
    load_spiders(engine, territory_spider_map)
    return engine


class Gazette(DeclarativeBase):
    __tablename__ = "gazettes"
    id = Column(Integer, primary_key=True)
    source_text = Column(Text)
    date = Column(Date)
    edition_number = Column(String)
    is_extra_edition = Column(Boolean)
    power = Column(String)
    file_checksum = Column(String)
    file_path = Column(String)
    file_url = Column(String)
    scraped_at = Column(DateTime)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    territory = relationship("Territory", back_populates="gazettes")
    territory_id = Column(String, ForeignKey("territories.id"))
    processed = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint("territory_id", "date", "file_checksum"),)


territory_spider_map = Table(
    "territory_spider_map",
    DeclarativeBase.metadata,
    Column("spider_name", ForeignKey("querido_diario_spiders.spider_name")),
    Column("territory_id", ForeignKey("territories.id")),
)


class Territory(DeclarativeBase):
    __tablename__ = "territories"
    id = Column(String, primary_key=True)
    name = Column(String)
    state_code = Column(String)
    state = Column(String)
    gazettes = relationship("Gazette", order_by=Gazette.id, back_populates="territory")


class QueridoDiarioSpider(DeclarativeBase):
    __tablename__ = "querido_diario_spiders"

    spider_name = Column(
        String,
        doc="As defined in 'name' attribute of each Spider class.",
        primary_key=True,
    )
    date_from = Column(Date, doc="Initial date this Spider is able to gather data.")
    date_to = Column(
        Date,
        doc="Final date this Spider is able to gather data ('null' if able to gather data in current day)",
        nullable=True,
    )
    enabled = Column(
        Boolean,
        default=False,
        doc="Flag to enable/disable Spider to be executed in production.",
    )

    territories = relationship("Territory", secondary=territory_spider_map)
