import datetime as dt

from decouple import config
from sqlalchemy import create_engine, Column, Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(config('DATABASE_URL'))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class BiddingExemption(DeclarativeBase):
    __tablename__ = 'bidding_exemptions'
    id = Column(Integer, primary_key=True)
    data = Column('data', JSONB)
    source_text = Column('source_text', Text)
    date = Column('date', Date)
    created_at = Column('created_at', DateTime, default=dt.datetime.utcnow)
    gazette = relationship('Gazette', back_populates='bidding_exemptions')
    gazette_id = Column(Integer, ForeignKey('gazettes.id'))


class Gazette(DeclarativeBase):
    __tablename__ = 'gazettes'
    id = Column(Integer, primary_key=True)
    contents = Column('contents', Text)
    date = Column('date', Date)
    is_extra_edition = Column('is_extra_edition', Boolean)
    is_parsed = Column('is_parsed', Boolean, default=False)
    municipality_id = Column('municipality_id', String)
    power = Column('power', String)
    file_checksum = Column('file_checksum', String)
    file_path = Column('file_path', String)
    file_url = Column('file_url', String)
    scraped_at = Column('scraped_at', DateTime)
    created_at = Column('created_at', DateTime, default=dt.datetime.utcnow)
    bidding_exemptions = relationship(
        'BiddingExemption', order_by=BiddingExemption.id, back_populates='gazette'
    )
    __table_args__ = (UniqueConstraint('municipality_id', 'date', 'file_checksum'),)
