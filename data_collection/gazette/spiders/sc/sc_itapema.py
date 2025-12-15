import base64
from datetime import date, datetime
from io import BytesIO
from typing import Optional, Tuple

from pypdf import PdfReader, PdfWriter
from pypdf.generic import Destination
from scrapy import FormRequest, Request
from scrapy.http import Response

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# TODO: Share abstraction with Florianopolis
class ScItapemaSpider(BaseGazetteSpider):
    name = "sc_itapema"
    TERRITORY_ID = "4208302"
    start_date = date(2015, 12, 17)  # TODO: É essa data mesmo?
    allowed_domains = ["edicao.dom.sc.gov.br"]
    city_name = "Itapema"

    def _requests(self, page):
        formdata = {
            "Edicao[cod_municipio]": "-1",
            "Edicao_page": str(page),
            "r": "site/edicoes",
        }
        return FormRequest(
            url="https://edicao.dom.sc.gov.br/?",
            method="GET",
            formdata=formdata,
            callback=self.parse_pagination,
            cb_kwargs={"page": page},
        )

    def start_requests(self):
        yield self._requests(1)

    def parse_pagination(self, response: Response, page):
        for item in response.css("tbody tr"):
            edition_number = item.css("td::text")[1].get()
            edition_url = item.css("td a")[1].attrib["href"]
            raw_date = item.css("td::text")[2].get()
            edition_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            if self.start_date <= edition_date <= self.end_date:
                yield Request(
                    url=edition_url,
                    callback=self.parse_pdf,
                    cb_kwargs={
                        "date": edition_date,
                        "edition_number": edition_number,
                        "is_extra_edition": False,
                        "power": "executive_legislative",
                    },
                )
        last_page = "next disabled" in response.url
        if edition_date > self.start_date and not last_page:
            yield self._requests(page + 1)

    def parse_pdf(
        self, response: Response, date, edition_number, is_extra_edition, power
    ):
        # TODO: What if its not a PDF?
        yield Gazette(
            date=date,
            edition_number=edition_number,
            is_extra_edition=is_extra_edition,
            power=power,
            file_urls=[],
            in_memory_files=[
                {
                    "url": response.url,
                    "name": f"{self.name}_{edition_number}_extracted.pdf",
                    "base64": GazettePDFExtractor(
                        response, self.city_name
                    ).process_item(),
                }
            ],
        )


class GazettePDFExtractor:
    def __init__(self, response: Response, city_name: str):
        self.response = response
        self.reader = PdfReader(BytesIO(response.body))
        self.city_name = city_name
        super().__init__()

    def find_city_page(self, city_name: str) -> Tuple[Destination, Destination]:
        outline = self.reader.outline
        found = None
        for item in outline:
            if item.title == city_name:
                found = item
            elif found:
                return found, item
        return (None, None)

    def process_item(self) -> Optional[str]:
        writer = PdfWriter()
        city_item, following_city_item = self.find_city_page(self.city_name)
        if city_item:
            city_page_number = self.reader.get_destination_page_number(city_item)
            following_city_page_number = self.reader.get_destination_page_number(
                following_city_item
            )  # TODO: What if following city is None?
            writer.add_page(self.reader.pages[0])
            for page_number in range(city_page_number, following_city_page_number):
                writer.add_page(self.reader.pages[page_number])
            with BytesIO() as buffer:
                writer.write(buffer)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
        return None
