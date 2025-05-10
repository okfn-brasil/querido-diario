import csv
import datetime as dt
import logging

import pkg_resources
from querido_diario_toolbox.slugs.slugs import make_entity_slug
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


def load_public_entity(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(PublicEntity).count() > 0:
        return

    logger.info("Populating 'entidades_publicas' table - Please wait!")
    public_entity_file = pkg_resources.resource_filename(
        "gazette", "resources/entidades_publicas.csv"
    )
    with open(public_entity_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        public_entities = []
        for row in reader:
            row["slug"] = make_entity_slug(row["nome"], row["unidade_federativa"])
            public_entities.append(PublicEntity(**row))
        session.bulk_save_objects(public_entities)
        session.commit()
    logger.info("Populating 'entidades_publicas' table - Done!")


def get_new_or_modified_spiders(session, public_entity_spider_map):
    registered_spiders = session.query(Scraper).all()
    registered_spiders_set = {
        (spider.nome, public_entity.id, spider.url_site, spider.data_inicial)
        for spider in registered_spiders
        for public_entity in spider.public_entities
    }
    only_new_or_modified_spiders = [
        spider_info
        for spider_info in public_entity_spider_map
        if spider_info not in registered_spiders_set
    ]
    return only_new_or_modified_spiders


def load_spiders(engine, public_entity_spider_map):
    Session = sessionmaker(bind=engine)
    session = Session()

    table_is_populated = session.query(Scraper).count() > 0
    spiders_to_persist = (
        get_new_or_modified_spiders(session, public_entity_spider_map)
        if table_is_populated
        else public_entity_spider_map
    )

    logger.info("Populating 'raspadores' table - Please wait!")

    public_entities = session.query(PublicEntity).all()
    public_entity_map = {t.id: t for t in public_entities}

    for info in spiders_to_persist:
        spider_name, public_entity_id, gazettes_page_url, date_from = info
        public_entity = public_entity_map.get(public_entity_id)
        if public_entity is not None:
            session.merge(
                Scraper(
                    nome=spider_name,
                    url_site=gazettes_page_url,
                    data_inicial=date_from,
                    public_entities=[public_entity],
                )
            )

    session.commit()
    logger.info("Populating 'raspadores' table - Done!")


def initialize_database(database_url, public_entity_spider_map):
    engine = create_engine(database_url)
    create_tables(engine)
    load_public_entity(engine)
    load_spiders(engine, public_entity_spider_map)
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
    public_entity = relationship("PublicEntity", back_populates="public_entities")
    entidades_publicas_id = Column(String, ForeignKey("entidades_publicas.id"))
    processed = Column(Boolean, default=False)
    __table_args__ = (
        UniqueConstraint("entidades_publicas_id", "date", "file_checksum"),
    )


public_entity_spider_map = Table(
    "raspador_por_entidadepublica",
    DeclarativeBase.metadata,
    Column("raspador", ForeignKey("raspadores.nome")),
    Column("entidade_publica_id", ForeignKey("entidades_publicas.id")),
)


class PublicEntity(DeclarativeBase):
    __tablename__ = "entidades_publicas"
    __table_args__ = (UniqueConstraint("slug"),)

    id = Column(String, primary_key=True)
    slug = Column(String)
    nome = Column(String)
    unidade_federativa = Column(String)
    regiao = Column(String)
    categoria = Column(String)

    gazettes = relationship(
        "Gazette", order_by=Gazette.id, back_populates="public_entity"
    )


class Scraper(DeclarativeBase):
    __tablename__ = "raspadores"
    __table_args__ = (UniqueConstraint("url_site"),)

    nome = Column(String, primary_key=True)
    url_site = Column(String)
    data_inicial = Column(Date)
    data_final = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True)

    public_entities = relationship("PublicEntity", secondary=public_entity_spider_map)
