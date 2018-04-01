import datetime as dt

from decouple import config
from sqlalchemy import create_engine, Column, Boolean, Date, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(config('DATABASE_URL'))


def create_gazettes_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Gazette(DeclarativeBase):
    __tablename__ = 'gazettes'
    id = Column(Integer, primary_key=True)
    contents = Column('contents', Text)
    date = Column('date', Date)
    is_extra_edition = Column('is_extra_edition', Boolean)
    municipality_id = Column('municipality_id', String)
    power = Column('power', String)
    file_checksum = Column('file_checksum', String)
    file_path = Column('file_path', String)
    file_url = Column('file_url', String)
    scraped_at = Column('scraped_at', DateTime)
    created_at = Column('created_at', DateTime, default=dt.datetime.utcnow)
    __table_args__ = (UniqueConstraint('municipality_id', 'date', 'file_checksum'),)
