import datetime as dt
import json
from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.settings import Settings
from sqlalchemy.orm import sessionmaker

try:
    import amqp
    import boto3
    import kafka
except ModuleNotFoundError:
    pass

from gazette.database.models import Gazette, initialize_database


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

        fields = [
            "source_text",
            "date",
            "edition_number",
            "is_extra_edition",
            "power",
            "scraped_at",
            "territory_id",
        ]
        gazette_item = {field: item.get(field) for field in fields}

        for file_info in item.get("files", []):
            already_downloaded = file_info["status"] == "uptodate"
            if already_downloaded:
                # We should not insert in database information of
                # files that were already downloaded before
                continue

            gazette_item["file_path"] = file_info["path"]
            gazette_item["file_url"] = file_info["url"]
            gazette_item["file_checksum"] = file_info["checksum"]

            gazette = Gazette(**gazette_item)
            session.add(gazette)
            try:
                session.commit()
            except Exception:
                spider.logger.exception(
                    f"Something wrong has happened when adding the gazette in the database."
                    f"Date: {gazette_item['date']}. "
                    f"File Checksum: {gazette_item['file_checksum']}.",
                )
                session.rollback()
                raise

        session.close()
        return item


class QueridoDiarioFilesPipeline(FilesPipeline):
    """Pipeline to download files described in file_urls or file_requests item fields.

    The main differences from the default FilesPipelines is that this pipeline:
        - organizes downloaded files differently (based on territory_id)
        - adds the file_requests item field to download files from request instances
        - allows a download_file_headers spider attribute to modify file_urls requests
    """

    DEFAULT_FILES_REQUESTS_FIELD = "file_requests"

    def __init__(self, *args, settings=None, **kwargs):
        super().__init__(*args, settings=settings, **kwargs)

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.files_requests_field = settings.get(
            "FILES_REQUESTS_FIELD", self.DEFAULT_FILES_REQUESTS_FIELD
        )

    def get_media_requests(self, item, info):
        """Makes requests from urls and/or lets through ready requests."""
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        download_file_headers = getattr(info.spider, "download_file_headers", {})
        yield from (Request(u, headers=download_file_headers) for u in urls)

        requests = ItemAdapter(item).get(self.files_requests_field, [])
        yield from requests

    def item_completed(self, results, item, info):
        """
        Transforms requests into strings if any present.
        Default behavior also adds results to item.
        """
        requests = ItemAdapter(item).get(self.files_requests_field, [])
        if requests:
            ItemAdapter(item)[self.files_requests_field] = [
                f"{r.method} {r.url}" for r in requests
            ]

        return super().item_completed(results, item, info)

    def file_path(self, request, response=None, info=None, item=None):
        """
        Path to save the files, modified to organize the gazettes in directories.
        The files will be under <territory_id>/<gazette date>/.
        """

        filepath = super().file_path(request, response=response, info=info, item=item)
        # The default path from the scrapy class begins with "full/". In this
        # class we replace that with the territory_id and gazette date.
        datestr = item["date"].strftime("%Y-%m-%d")
        filename = Path(filepath).name
        return str(Path(item["territory_id"], datestr, filename))


class QueueExporterPipeline(ABC):
    def open_spider(self, spider):
        self.settings = spider.crawler.settings

    @abstractmethod
    def close_spider(self, spider):
        pass

    @abstractmethod
    def send_message(self, data):
        pass

    @abstractmethod
    def convert_item_to_message(self, item):
        pass

    def _convert_item_to_string(self, item):
        data = dict(item)
        for field in data.keys():
            value = data[field]
            if isinstance(value, dt.date):
                data[field] = value.isoformat()
        return json.dumps(data)

    def _convert_item_to_bytes(self, item):
        data = self._convert_item_to_string(item)
        return bytes(data, "utf-8")

    def process_item(self, item, spider):
        message = self.convert_item_to_message(item)
        self.send_message(message)
        return item


class AmqpExporterPipeline(QueueExporterPipeline):
    def open_spider(self, spider):
        super().open_spider(spider)
        self.connection = amqp.Connection(
            host=self.settings.get("AMQP_HOST"),
            userid=self.settings.get("AMQP_USERNAME"),
            password=self.settings.get("AMQP_PASSWORD"),
        )
        self.connection.connect()
        self.channel = self.connection.channel()
        self.channel.open()
        self.channel.queue_declare(queue=self.settings.get("AMQP_QUEUE"))

    def close_spider(self, spider):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    def send_message(self, data):
        self.channel.basic_publish(
            exchange=self.settings.get("AMQP_EXCHANGE"),
            routing_key=self.settings.get("AMQP_ROUTING_KEY"),
            msg=amqp.Message(data),
        )

    def convert_item_to_message(self, item):
        return self._convert_item_to_bytes(item)


class KafkaExporterPipeline(QueueExporterPipeline):
    def open_spider(self, spider):
        super().open_spider(spider)
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=self.settings.get("KAFKA_BOOTSTRAP_SERVERS")
        )

    def close_spider(self, spider):
        if self.producer:
            self.producer.flush()
            self.producer.close()

    def send_message(self, data):
        self.producer.send(self.settings.get("KAFKA_TOPIC"), data)

    def convert_item_to_message(self, item):
        return self._convert_item_to_bytes(item)


class SQSExporterPipeline(QueueExporterPipeline):
    def open_spider(self, spider):
        super().open_spider(spider)
        self.resource = boto3.resource(
            service_name="sqs",
            region_name=self.settings.get("AWS_REGION_NAME"),
            aws_access_key_id=self.settings.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=self.settings.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.queue = self.resource.get_queue_by_name(
            QueueName=self.settings.get("SQS_QUEUE_NAME")
        )

    def close_spider(self, spider):
        pass

    def send_message(self, data):
        self.queue.send_message(MessageBody=data)

    def convert_item_to_message(self, item):
        return self._convert_item_to_string(item)


class KinesisExporterPipeline(QueueExporterPipeline):
    def open_spider(self, spider):
        super().open_spider(spider)
        self.client = boto3.client(
            service_name="kinesis",
            region_name=self.settings.get("AWS_REGION_NAME"),
            aws_access_key_id=self.settings.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=self.settings.get("AWS_SECRET_ACCESS_KEY"),
        )

    def close_spider(self, spider):
        pass

    def send_message(self, data):
        self.client.put_record(
            StreamName=self.settings.get("KINESIS_STREAM_NAME"),
            PartitionKey=str(uuid4()),
            Data=data,
        )

    def convert_item_to_message(self, item):
        return self._convert_item_to_string(item)
