from datetime import date, datetime

from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseBarcoDigitalSpider(BaseGazetteSpider):
    EDITION_TYPE_NORMAL = 1
    EDITION_TYPE_EXTRA = 2
    EDITION_TYPE_SUPPLEMENT = 3

    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)
        end_date = self.end_date

        periods_of_interest = [
            (date.year, date.month)
            for date in rrule(freq=MONTHLY, dtstart=initial_date, until=end_date)
        ]

        for year, month in periods_of_interest:
            url = (
                f"{self.base_url}/api/publico/diario/calendario?mes={month}&ano={year}"
            )
            yield Request(url)

    def parse(self, response):
        for documents in response.json().values():
            for document in documents:
                document_date = datetime.strptime(
                    document.get("data"), "%Y-%m-%d"
                ).date()

                if document_date > self.end_date:
                    continue
                elif document_date < self.start_date:
                    return

                yield Gazette(
                    date=document_date,
                    edition_number=document.get("edicao"),
                    is_extra_edition=document.get("tipo_edicao_id")
                    != self.EDITION_TYPE_NORMAL,
                    file_urls=[f"{self.base_url}/arquivo/{document.get('url')}"],
                    power="executive",
                )
