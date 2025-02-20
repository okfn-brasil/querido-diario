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
            public_entities.append(PublicEntity(**row))
        session.bulk_save_objects(public_entities)
        session.commit()
    logger.info("Populating 'entidades_publicas' table - Done!")


def get_new_or_modified_spiders(session, public_entity_spider_map):
    registered_spiders = session.query(Spiders).all()
    registered_spiders_set = {
        (spider.nome, public_entity.id, spider.url_do_site, spider.data_inicial)
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

    table_is_populated = session.query(Spiders).count() > 0
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
                Spiders(
                    nome=spider_name,
                    url_do_site=gazettes_page_url,
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
    __table_args__ = (UniqueConstraint("entidade_publica_id", "data", "file_checksum"),)

    public_entity = relationship("PublicEntity", back_populates="public_entities")

    id = Column(Integer, primary_key=True)
    entidade_publica_id = Column(String, ForeignKey("entidades_publicas.id"))
    data = Column(Date)
    poder = Column(String)
    numero_edicao = Column(String)
    edicao_extra = Column(Boolean)
    categoria_ato = Column(String)
    orgao_publicador = Column(String)
    file_checksum = Column(String)
    file_path = Column(String)
    file_url = Column(String)
    scraped_at = Column(DateTime)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    processed = Column(Boolean, default=False)


public_entity_spider_map = Table(
    "raspador_por_entidadepublica",
    DeclarativeBase.metadata,
    Column("raspador", ForeignKey("raspadores.nome")),
    Column("entidade_publica_id", ForeignKey("entidades_publicas.id")),
)


class PublicEntity(DeclarativeBase):
    __tablename__ = "entidades_publicas"

    public_entities = relationship(
        "Gazette", order_by=Gazette.id, back_populates="public_entity"
    )

    id = Column(String, primary_key=True)
    slug = Column(String)
    nome = Column(String)
    unidade_federativa = Column(String)
    regiao = Column(String)
    categoria = Column(String)


class Spiders(DeclarativeBase):
    __tablename__ = "raspadores"

    public_entities = relationship("PublicEntity", secondary=public_entity_spider_map)

    nome = Column(
        String,
        doc="As defined in 'name' attribute of each Spider class.",
        primary_key=True,
    )
    url_do_site = Column(
        String, doc="As defined in 'GAZETTES_PAGE_URL' attribute of each Spider class."
    )
    data_inicial = Column(Date, doc="Initial date this Spider is able to gather data.")
    data_final = Column(
        Date,
        doc="Final date this Spider is able to gather data ('null' if able to gather data in current day)",
        nullable=True,
    )
    ativo = Column(
        Boolean,
        default=False,
        doc="Flag to enable/disable Spider to be executed in production.",
    )
