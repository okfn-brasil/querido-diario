import os
import subprocess

from database.models import Gazette, db_connect, create_tables
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker


from gazette.settings import FILES_STORE


class PdfParsingPipeline:

    def process_item(self, item, spider):
        item['source_text'] = self.pdf_source_text(item)
        for key, value in item['files'][0].items():
            item[f'file_{key}'] = value
        item.pop('files')
        item.pop('file_urls')
        return item

    def pdf_source_text(self, item):
        pdf_path = os.path.join(FILES_STORE, item['files'][0]['path'])
        command = f'pdftotext -layout {pdf_path}'
        subprocess.run(command, shell=True, check=True)
        if '.pdf' in pdf_path:
            text_path = pdf_path.replace('.pdf', '.txt')
        else:
            text_path = pdf_path + '.txt'
        with open(text_path) as file:
            return file.read()


class PostgreSQLPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
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


class GazetteDateFilteringPipeline(object):

    def process_item(self, item, spider):
        if hasattr(spider, 'start_date'):
            if spider.start_date > item.get('date'):
                raise DropItem(
                    'Droping all items before {}'.format(spider.start_date))
        return item
