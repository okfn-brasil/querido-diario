import datetime as dt

from decouple import config
from sqlalchemy import (
    create_engine,
    Column,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(config("DATABASE_URL"))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


def initialize_database():
    engine = db_connect()
    create_tables(engine)
    return engine


class BiddingExemption(DeclarativeBase):
    __tablename__ = "bidding_exemptions"
    id = Column(Integer, primary_key=True)
    data = Column("data", JSONB)
    source_text = Column("source_text", Text)
    date = Column("date", Date)
    contracted = Column("contracted", String)
    contracted_code = Column("contracted_code", String)
    value = Column("value", Numeric)
    is_parsed = Column("is_parsed", Boolean, default=False)
    object = Column("object", String)
    created_at = Column("created_at", DateTime, default=dt.datetime.utcnow)
    gazette = relationship("Gazette", back_populates="bidding_exemptions")
    gazette_id = Column(Integer, ForeignKey("gazettes.id"))


class Gazette(DeclarativeBase):
    __tablename__ = "gazettes"
    id = Column(Integer, primary_key=True)
    source_text = Column(Text)
    date = Column(Date)
    is_extra_edition = Column(Boolean)
    is_parsed = Column(Boolean, default=False)
    power = Column(String)
    file_checksum = Column(String)
    file_path = Column(String)
    file_url = Column(String)
    scraped_at = Column(DateTime)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    territory = relationship("Territory", back_populates="gazettes")
    territory_id = Column(String, ForeignKey("territories.id"))
    bidding_exemptions = relationship(
        "BiddingExemption", order_by=BiddingExemption.id, back_populates="gazette"
    )
    __table_args__ = (UniqueConstraint("territory_id", "date", "file_checksum"),)


class Territory(DeclarativeBase):
    __tablename__ = "territories"
    id = Column(String, primary_key=True)
    name = Column(String)
    state_code = Column(String)
    state = Column(String)
    gazettes = relationship("Gazette", order_by=Gazette.id, back_populates="territory")
