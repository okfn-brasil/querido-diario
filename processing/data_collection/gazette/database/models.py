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

    num_territories = session.query(Territory).count()
    if num_territories == 0:
        logger.info("Populating 'territories' table. Please wait!")
        territories_file = pkg_resources.resource_filename(
            "gazette", "resources/territories.csv"
        )
        with open(territories_file) as csvfile:
            reader = csv.DictReader(csvfile)
            territories = []
            for row in reader:
                territories.append(Territory(**row))
            session.bulk_save_objects(territories)
            session.commit()


def initialize_database(database_url):
    engine = create_engine(database_url)
    create_tables(engine)
    load_territories(engine)
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


class Territory(DeclarativeBase):
    __tablename__ = "territories"
    id = Column(String, primary_key=True)
    name = Column(String)
    state_code = Column(String)
    state = Column(String)
    gazettes = relationship("Gazette", order_by=Gazette.id, back_populates="territory")
