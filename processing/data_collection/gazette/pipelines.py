import os
import subprocess

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


class FilesPipeline(object):
    def process_item(self, item, spider):
        if FILES_STORE:
            from gazette.service import Spaces

            pdf_path = os.path.join(FILES_STORE, item["files"][0]["path"])
            Spaces().upload_file(pdf_path)
            return None

        return item
