import json
import os

from scrapy import signals
from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DeclarativeBase = declarative_base()


class JobStats(DeclarativeBase):
    __tablename__ = "job_stats"
    id = Column(Integer, primary_key=True)
    spider = Column(String)
    start_time = Column(DateTime)
    job_id = Column(String)
    job_stats = Column(JSON)


class StatsPersist:
    def __init__(self, crawler, database_url):
        self._stats = crawler.stats
        self._database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("QUERIDODIARIO_DATABASE_URL")

        o = cls(crawler, database_url)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        engine = create_engine(self._database_url)
        DeclarativeBase.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def spider_closed(self, spider, reason):
        stats = self._stats.get_stats()
        serializable_stats = json.loads(json.dumps(stats, default=str))
        job_stats = JobStats(
            spider=spider.name,
            start_time=stats["start_time"],
            job_id=os.environ.get("SHUB_JOBKEY", ""),
            job_stats=serializable_stats,
        )
        session = self.Session()
        session.add(job_stats)
        session.commit()
