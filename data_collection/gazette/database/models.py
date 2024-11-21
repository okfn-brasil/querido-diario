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


def load_public_entities(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(PublicEntity).count() > 0:
        return

    logger.info("Populating 'public_entities' table - Please wait!")
    public_entities_file = pkg_resources.resource_filename(
        "gazette", "resources/public_entities.csv"
    )
    with open(public_entities_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        public_entities = []
        for row in reader:
            public_entities.append(PublicEntity(**row))
        session.bulk_save_objects(public_entities)
        session.commit()
    logger.info("Populating 'public_entities' table - Done!")


def get_new_or_modified_spiders(session, entity_spider_map):
    registered_spiders = session.query(QueridoDiarioSpider).all()
    registered_spiders_set = {
        (spider.spider_name, entity.id, spider.date_from)
        for spider in registered_spiders
        for entity in spider.public_entities
    }
    only_new_or_modified_spiders = [
        spider_info
        for spider_info in entity_spider_map
        if spider_info not in registered_spiders_set
    ]
    return only_new_or_modified_spiders


def load_spiders(engine, entity_spider_map):
    Session = sessionmaker(bind=engine)
    session = Session()

    table_is_populated = session.query(QueridoDiarioSpider).count() > 0
    spiders_to_persist = (
        get_new_or_modified_spiders(session, entity_spider_map)
        if table_is_populated
        else entity_spider_map
    )

    logger.info("Populating 'querido_diario_spider' table - Please wait!")

    public_entities = session.query(PublicEntity).all()
    entity_map = {t.id: t for t in public_entities}

    for info in spiders_to_persist:
        spider_name, id, date_from = info
        entity = entity_map.get(id)
        if entity is not None:
            session.merge(
                QueridoDiarioSpider(
                    spider_name=spider_name,
                    date_from=date_from,
                    public_entities=[entity],
                )
            )

    session.commit()
    logger.info("Populating 'querido_diario_spider' table - Done!")


def initialize_database(database_url, entity_spider_map):
    engine = create_engine(database_url)
    create_tables(engine)
    load_public_entities(engine)
    load_spiders(engine, entity_spider_map)
    return engine


class Gazette(DeclarativeBase):
    __tablename__ = "scraped_gazettes"
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
    processed = Column(Boolean, default=False)

    public_entity = relationship("PublicEntity", back_populates="scraped_gazettes")
    public_entity_id = Column(String, ForeignKey("public_entities.id"))

    __table_args__ = (
        UniqueConstraint("public_entity_id", "date", "file_checksum"),
    )


entity_spider_map = Table(
    "entity_spider_map",
    DeclarativeBase.metadata,
    Column("spider_name", ForeignKey("querido_diario_spiders.spider_name")),
    Column("public_entity_id", ForeignKey("public_entities.id")),
)


class PublicEntity(DeclarativeBase):
    __tablename__ = "public_entities"
    id = Column(String, primary_key=True)
    name = Column(String)
    slug = Column(String)
    category = Column(String)
    acronym = Column(String)
    federal_unity = Column(String)
    scope = Column(String)
    scraped_gazettes = relationship(
        "Gazette", order_by=Gazette.public_entity_id, back_populates="public_entity"
    )


class QueridoDiarioSpider(DeclarativeBase):
    __tablename__ = "querido_diario_spiders"

    spider_name = Column(
        String,
        doc="As defined in 'name' attribute of each spider class.",
        primary_key=True,
    )
    website_url = Column(
        String,
        doc="As defined in 'user_website' attribute of each spider class.",
    )
    date_from = Column(Date, doc="Initial date this spider is able to gather data.")
    date_to = Column(
        Date,
        doc="Final date this spider is able to gather data ('null' if able to gather data in current day)",
        nullable=True,
    )
    enabled = Column(
        Boolean,
        default=False,
        doc="Flag to enable/disable spider to be executed in production.",
    )

    public_entities = relationship("PublicEntity", secondary=entity_spider_map)
