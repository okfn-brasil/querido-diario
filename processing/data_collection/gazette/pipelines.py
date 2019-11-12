import os
import subprocess
import hashlib

from database.models import Gazette, initialize_database
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker


from gazette.settings import FILES_STORE


class PdfParsingPipeline:
    def process_item(self, item, spider):
        item["source_text"] = self.pdf_source_text(item)
        for key, value in item["files"][0].items():
            item[f"file_{key}"] = value
        item.pop("files")
        item.pop("file_urls")
        return item

    def pdf_source_text(self, item):
        pdf_path = os.path.join(FILES_STORE, item["files"][0]["path"])
        command = f"pdftotext -layout {pdf_path}"
        subprocess.run(command, shell=True, check=True)
        if ".pdf" in pdf_path:
            text_path = pdf_path.replace(".pdf", ".txt")
        else:
            text_path = pdf_path + ".txt"
        with open(text_path) as file:
            return file.read()


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


class DocToPdfPipeline:
    """
    Convert a doc[x] file to pdf
    """

    def process_item(self, item, spider):
        # if item is not a doc, skip it
        if not self.is_doc(item["files"][0]["path"]):
            return item
        # it's doc[x]. Convert it to pdf
        doc_path = os.path.join(FILES_STORE, item["files"][0]["path"])
        # use libreoffice writer to convert
        command = f"lowriter --convert-to pdf --outdir {FILES_STORE}/full {doc_path}"
        subprocess.run(command, shell=True, check=True)
        if doc_path.endswith("doc"):
            pdf_path = doc_path[:-3] + "pdf"
        elif doc_path.endswith("docx"):
            pdf_path = doc_path[:-4] + "pdf"
        else:
            pdf_path = doc_path + ".pdf"
        os.unlink(doc_path)
        # update to the new file path and its checksum
        item["files"][0]["path"] = pdf_path
        item["files"][0]["checksum"] = self.calculate_md5sum(pdf_path)
        return item

    @staticmethod
    def is_doc(filepath):
        """
        If the file path ends with doc or docx returns True. Otherwise,
        returns False
        """
        filepath = filepath.lower()
        return filepath.endswith("doc") or filepath.endswith("docx")

    @staticmethod
    def calculate_md5sum(filepath):
        """
        Get the md5sum of the given file

        Returns string of the md5sum
        """
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
