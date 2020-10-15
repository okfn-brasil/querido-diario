import datetime as dt
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from gazette.database.models import initialize_database, Gazette


class GazetteDateFilteringPipeline:
    def process_item(self, item, spider):
        if hasattr(spider, "start_date"):
            if spider.start_date > item.get("date"):
                raise DropItem("Droping all items before {}".format(spider.start_date))
        return item


class DefaultValuesPipeline:
    """ Add defaults values field, if not already set in the item """

    default_field_values = {
        "territory_id": lambda spider: getattr(spider, "TERRITORY_ID"),
        "scraped_at": lambda spider: dt.datetime.utcnow(),
    }

    def process_item(self, item, spider):
        for field in self.default_field_values:
            if field not in item:
                item[field] = self.default_field_values.get(field)(spider)
        return item


class SQLDatabasePipeline:
    def __init__(self, database_url):
        self.database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("QUERIDODIARIO_DATABASE_URL")
        return cls(database_url=database_url)

    def open_spider(self, spider):
        if self.database_url is not None:
            engine = initialize_database(self.database_url)
            self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if self.database_url is None:
            return item

        session = self.Session()

        item_file = item["files"][0]
        item["file_path"] = item_file["path"]
        item["file_url"] = item_file["url"]
        item["file_checksum"] = item_file["checksum"]
        item.pop("files")
        item.pop("file_urls")

        gazette = Gazette(**item)
        try:
            session.add(gazette)
            session.commit()
        except IntegrityError:
            spider.logger.warning(
                f"Gazette from {item['date']} already exists in the database."
            )
            session.rollback()
        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class RequestWithItem(Request):
    """
    Specialized Request object to allow carry the item which generate the request.
    Thus, we can use the gazette date in the path where the file will be stored.
    """

    def __init__(self, url, item):
        super().__init__(url)
        self.item = item


class QueridoDiarioFilesPipeline(FilesPipeline):
    """
    When the downloaded file are stored in a remote storage system (e.g.
    Digital Ocean spaces), we need to specialize FilesPipeline class in order
    to allow us define a different directory where the files will be store. In
    the current implementation we organize gazette files by date. All the
    gazettes from the same date will be store in the same directory.
    """

    def file_path(self, request, response=None, info=None):
        filepath = super().file_path(request, response, info)
        # The default path from the scrapy class begins with "full/". In this
        # class we replace that with the gazette date.
        datestr = request.item["date"].strftime("%d-%m-%Y")
        filename = Path(filepath).name
        return str(Path(datestr, filename))

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field)
        if not urls:
            return
        yield from (RequestWithItem(u, item) for u in urls)
