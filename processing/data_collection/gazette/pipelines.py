from pathlib import Path
import hashlib
import magic
import os
import subprocess

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from database.models import Gazette, initialize_database
from gazette.settings import FILES_STORE


class PostgreSQLPipeline:
    def __init__(self):
        engine = initialize_database()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        # TEMP: The attribute "municipality_id" was recently renamed to "territory_id"
        #       in the database. The two following lines may be deleted once we have
        #       no branches using "municipality_id".
        if "municipality_id" in item:
            item["territory_id"] = item.pop("municipality_id")
        gazette = Gazette(**item)
        try:
            session.add(gazette)
            session.commit()
        except IntegrityError as exc:
            spider.logger.warning(
                "Gazette from %s already exists in the database", item["date"]
            )
            session.rollback()
        except:
            session.rollback()
            raise

        finally:
            session.close()
        return item


class GazetteDateFilteringPipeline:
    def process_item(self, item, spider):
        if hasattr(spider, "start_date"):
            if spider.start_date > item.get("date"):
                raise DropItem("Droping all items before {}".format(spider.start_date))
        return item


class ExtractTextPipeline:
    """
    Identify file format and call the right tool to extract the text from it
    """

    def process_item(self, item, spider):
        if self.is_doc(item["files"][0]["path"]):
            item["source_text"] = self.doc_source_text(item)
        elif self.is_pdf(item["files"][0]["path"]):
            item["source_text"] = self.pdf_source_text(item)
        elif self.is_txt(item["files"][0]["path"]):
            item["source_text"] = self.txt_source_text(item)
        else:
            raise Exception(
                "Unsupported file type: " + self.get_file_type(item["files"][0]["path"])
            )

        for key, value in item["files"][0].items():
            item[f"file_{key}"] = value
        item.pop("files")
        item.pop("file_urls")
        return item

    def pdf_source_text(self, item):
        """
        Gets the text from pdf files
        """
        pdf_path = os.path.join(FILES_STORE, item["files"][0]["path"])
        text_path = pdf_path + ".txt"
        command = f"pdftotext -layout {pdf_path} {text_path}"
        subprocess.run(command, shell=True, check=True)
        with open(text_path) as file:
            return file.read()

    def doc_source_text(self, item):
        """
        Gets the text from docish files
        """
        doc_path = os.path.join(FILES_STORE, item["files"][0]["path"])
        text_path = doc_path + ".txt"
        command = f"java -jar /tika-app.jar --text {doc_path}"
        with open(text_path, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f)
        with open(text_path, "r") as f:
            return f.read()

    def txt_source_text(self, item):
        """
        Gets the text from txt files
        """
        with open(
            os.path.join(FILES_STORE, item["files"][0]["path"]), encoding="ISO-8859-1"
        ) as f:
            return f.read()

    def is_pdf(self, filepath):
        """
        If the file type is pdf returns True. Otherwise,
        returns False
        """
        return self._is_file_type(filepath, file_types=["application/pdf"])

    def is_doc(self, filepath):
        """
        If the file type is doc or similar returns True. Otherwise,
        returns False
        """
        file_types = [
            "application/msword",
            "application/vnd.oasis.opendocument.text",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]
        return self._is_file_type(filepath, file_types)

    def is_txt(self, filepath):
        """
        If the file type is txt returns True. Otherwise,
        returns False
        """
        return self._is_file_type(filepath, file_types=["text/plain"])

    def get_file_type(self, filename):
        """
        Returns the file's type
        """
        file_path = os.path.join(FILES_STORE, filename)
        return magic.from_file(file_path, mime=True)

    def _is_file_type(self, filepath, file_types):
        """
        Generic method to check if a identified file type matches a given list of types
        """
        return self.get_file_type(filepath) in file_types


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
