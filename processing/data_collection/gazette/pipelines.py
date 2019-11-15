import os
import subprocess
import hashlib

from database.models import Gazette, initialize_database
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker


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
        else:
            raise "Unsupported file type"

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
        command = f"pdftotext -layout {pdf_path}"
        subprocess.run(command, shell=True, check=True)
        text_path = pdf_path + ".txt"
        with open(text_path) as file:
            return file.read()

    def doc_source_text(self, item):
        """
        Gets the text from docish files
        """
        doc_path = os.path.join(FILES_STORE, item["files"][0]["path"])
        text_path = doc_path + ".txt"
        command = f"java -jar /tika-app-1.22.jar --text {doc_path}"
        with open(text_path, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f)
        with open(text_path, "r") as f:
            return f.read()

    @staticmethod
    def is_pdf(filepath):
        """
        If the file path ends with pdf returns True. Otherwise,
        returns False
        """
        return filepath.lower().endswith("pdf")

    @staticmethod
    def is_doc(filepath):
        """
        If the file path ends with doc or docx returns True. Otherwise,
        returns False
        """
        filepath = filepath.lower()
        return filepath.endswith("doc") or filepath.endswith("docx")
