import datetime as dt
from pathlib import Path

import boto3
import filetype
from itemadapter import ItemAdapter
from scrapy import spiderloader
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.files import FilesPipeline
from scrapy.settings import Settings
from scrapy.utils import project
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from gazette.database.models import Gazette, initialize_database


class GazetteDateFilteringPipeline:
    def process_item(self, item, spider):
        if hasattr(spider, "start_date"):
            if spider.start_date > item.get("date"):
                raise DropItem("Droping all items before {}".format(spider.start_date))
        return item


class DefaultValuesPipeline:
    def process_item(self, item, spider):
        item["territory_id"] = getattr(spider, "TERRITORY_ID")

        # Date manipulation to allow jsonschema to validate correctly
        item["date"] = str(item["date"])
        item["scraped_at"] = dt.datetime.utcnow().isoformat("T") + "Z"

        return item


class SQLDatabasePipeline:
    def __init__(self, database_url):
        self.database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("QUERIDODIARIO_DATABASE_URL")
        return cls(database_url=database_url)

    def _generate_territory_spider_map(self):
        settings = project.get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        spiders = spider_loader.list()
        classes = [spider_loader.load(name) for name in spiders]

        mapping = []
        for spider_class in classes:
            spider_name = getattr(spider_class, "name", None)
            territory_id = getattr(spider_class, "TERRITORY_ID", None)
            date_from = getattr(spider_class, "start_date", None)
            if all((spider_name, territory_id, date_from)):
                mapping.append((spider_name, territory_id, date_from))
        return mapping

    def open_spider(self, spider):
        if self.database_url is not None:
            territory_spider_map = self._generate_territory_spider_map()
            engine = initialize_database(self.database_url, territory_spider_map)
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
        gazette_item["date"] = dt.datetime.strptime(
            gazette_item["date"], "%Y-%m-%d"
        ).date()
        gazette_item["scraped_at"] = dt.datetime.strptime(
            gazette_item["scraped_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

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
            except SQLAlchemyError as exc:
                spider.logger.warning(
                    f"Something wrong has happened when adding the gazette in the database. "
                    f"Date: {gazette_item['date']}. "
                    f"File Checksum: {gazette_item['file_checksum']}. "
                    f"Details: {exc.args}"
                )
                session.rollback()

        session.close()

        return item


class QueridoDiarioFilesPipeline(FilesPipeline):
    """Pipeline to download files described in file_urls or file_requests item fields.

    The main differences from the default FilesPipelines is that this pipeline:
        - organizes downloaded files differently (based on territory_id)
        - adds the file_requests item field to download files from request instances
        - allows a download_file_headers spider attribute to modify file_urls requests
        - saves files to two S3 buckets (primary and secondary)
    """

    DEFAULT_FILES_REQUESTS_FIELD = "file_requests"

    def __init__(self, *args, settings=None, **kwargs):
        super().__init__(*args, settings=settings, **kwargs)

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.files_requests_field = settings.get(
            "FILES_REQUESTS_FIELD", self.DEFAULT_FILES_REQUESTS_FIELD
        )

        # Secondary bucket configuration
        self.secondary_bucket = settings.get("FILES_STORE_SECONDARY", "")
        self.s3_client = None
        if self.secondary_bucket and self.secondary_bucket.startswith("s3://"):
            self._setup_s3_client(settings)

    def _setup_s3_client(self, settings):
        """Setup boto3 S3 client for secondary bucket.

        Compatível com Digital Ocean Spaces, AWS S3 e outros serviços S3-compatíveis.
        Se endpoint_url não for fornecido (None ou vazio), boto3 usa o endpoint padrão da AWS.
        """
        try:
            session_config = {
                "aws_access_key_id": settings.get("AWS_ACCESS_KEY_ID"),
                "aws_secret_access_key": settings.get("AWS_SECRET_ACCESS_KEY"),
                "region_name": settings.get("AWS_REGION_NAME"),
            }

            # Adiciona endpoint_url apenas se fornecido (necessário para Digital Ocean Spaces e Minio)
            # Para AWS S3, deixar vazio ou não definir a variável AWS_ENDPOINT_URL
            endpoint_url = settings.get("AWS_ENDPOINT_URL")
            if endpoint_url:
                session_config["endpoint_url"] = endpoint_url

            self.s3_client = boto3.client("s3", **session_config)
            self.s3_acl = settings.get("FILES_STORE_S3_ACL", "public-read")
        except Exception as e:
            # Log error but don't fail - primary bucket will still work
            print(f"Warning: Could not setup S3 client for secondary bucket: {e}")
            self.s3_client = None

    def _copy_to_secondary_bucket(self, file_path, file_data, spider):
        """Copy file to secondary S3 bucket."""
        if not self.s3_client or not self.secondary_bucket:
            return

        try:
            bucket_name = self.secondary_bucket.replace("s3://", "").rstrip("/")
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_path,
                Body=file_data,
                ACL=self.s3_acl,
            )
            spider.logger.info(f"File copied to secondary bucket: {file_path}")
        except Exception as e:
            spider.logger.error(
                f"Failed to copy file to secondary bucket {file_path}: {e}"
            )

    def file_downloaded(self, response, request, info, *, item=None):
        """Override to copy file to secondary bucket after download."""
        result = super().file_downloaded(response, request, info, item=item)

        # Copy to secondary bucket if configured
        if result and self.s3_client:
            file_path = result.get("path")
            if file_path:
                self._copy_to_secondary_bucket(file_path, response.body, info.spider)

        return result

    def get_media_requests(self, item, info):
        """Makes requests from urls and/or lets through ready requests."""
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        download_file_headers = getattr(info.spider, "download_file_headers", {})
        yield from (
            Request(u, callback=NO_CALLBACK, headers=download_file_headers)
            for u in urls
        )

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
        Path to save the files, modified to organize the gazettes in directories
        and with the right file extension added.
        The files will be under <territory_id>/<gazette date>/<filename>.
        """
        filepath = Path(
            super().file_path(request, response=response, info=info, item=item)
        )
        # The default path from the scrapy class begins with "full/". In this
        # class we replace that with the territory_id and gazette date.
        filename = filepath.name

        if response is not None and not filepath.suffix:
            filename = self._get_filename_with_extension(filename, response)

        return str(Path(item["territory_id"], item["date"], filename))

    def _get_filename_with_extension(self, filename, response):
        # The majority of the Gazettes are PDF files, so we can check it
        # faster validating document Content-Type before using a more costly
        # check with filetype library
        file_extension = (
            ".pdf" if response.headers.get("Content-Type") == b"application/pdf" else ""
        )

        if not file_extension:
            # Checks file extension from file header if possible
            max_file_header_size = 261
            file_kind = filetype.guess(response.body[:max_file_header_size])
            file_extension = f".{file_kind.extension}" if file_kind is not None else ""

        return f"{filename}{file_extension}"
