import os
import subprocess

from sqlalchemy.orm import sessionmaker

from gazette.settings import FILES_STORE
from gazette.models import Gazette, db_connect, create_gazettes_table


class PdfParsingPipeline:

    def process_item(self, item, spider):
        item['contents'] = self.pdf_contents(item)
        for key, value in item['files'][0].items():
            item[f'file_{key}'] = value
        item.pop('files')
        item.pop('file_urls')
        return item

    def pdf_contents(self, item):
        pdf_path = os.path.join(FILES_STORE, item['files'][0]['path'])
        command = f'pdftotext -layout {pdf_path}'
        subprocess.run(command, shell=True, check=True)
        text_path = pdf_path.replace('.pdf', '.txt')
        with open(text_path) as file:
            return file.read()


class PostgreSQLPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_gazettes_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
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
