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
        elif self.is_txt(item["files"][0]["path"]):
            item["source_text"] = self.txt_source_text(item)
        else:
            raise Exception(
                "Unsupported file type: " + self.get_extension(item["files"][0]["path"])
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

    def is_pdf(self, filepath):
        """
        If the file path ends with pdf returns True. Otherwise,
        returns False
        """
        return self.get_extension(filepath) == "pdf"

    def is_doc(self, filepath):
        """
        If the file path ends with doc,  docx or odt returns True. Otherwise,
        returns False
        """
        extension = self.get_extension(filepath)
        return extension == "doc" or extension == "docx" or extension == "odt"

    def get_extension(self, filename):
        """
        Returns the file's extension
        """
        filename = filename.lower()
        return filename[filename.rfind(".") + 1 :]

    def is_txt(self, filepath):
        """
        If the file path ends with txt returns True. Otherwise,
        returns False
        """
        return self.get_extension(filepath) == "txt"

    def txt_source_text(self, item):
        """
        Gets the text from txt files
        """
        with open(
            os.path.join(FILES_STORE, item["files"][0]["path"]), encoding="ISO-8859-1"
        ) as f:
            return f.read()
