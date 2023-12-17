from datetime import datetime, date
from urllib.parse import urlencode
import scrapy
from dateutil import parser
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToParaisoSpider(BaseGazetteSpider):
    TERRITORY_ID = "1716109"
    name = "to_paraiso"
    allowed_domains = ["paraisodotocantins.diarioeletronico.org"]
    start_date = date(2021, 1, 14)  # First gazette available
    custom_settings = {
        "MEDIA_ALLOW_REDIRECTS": True,
    }

    def start_requests(self):
        dt_inicial = self.start_date.strftime("%d/%m/%Y")
        dt_final = self.end_date.strftime("%d/%m/%Y")
        url_params = {
            "std": dt_inicial,
            "end": dt_final,

        }
        params = urlencode(url_params)
        url = f"https://paraisodotocantins.diarioeletronico.org/edicoes/?{params}"
        yield scrapy.Request(url)

    def _translate_month(self, month):
        return {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12",
        }[month]

    def _get_date_from_parent_edition(self, gazette_text):
        day, month_name, year = gazette_text.split(" de ")
        month = self._translate_month(month_name.lower())
        formatted_date = f"{year}-{month}-{day}"
        return datetime.strptime(str(formatted_date), "%Y-%m-%d").date()

    def parse(self, response):
        for gazette in response.css(".table tbody tr"):
            edition_number = gazette.xpath("./th[1]/text()").get()
            raw_gazette_date = gazette.xpath("./th[2]/text()").get()
            gazette_date = self._get_date_from_parent_edition(raw_gazette_date)
            is_extra_edition = 'Edição Extra' in str(gazette.xpath("./td[@class='download']/p/a/text()").get())
            gazette_url = gazette.css("a::attr(href)").extract_first()[:-4]
            if is_extra_edition:
                gazette_url_extra = gazette.css("a::attr(href)").extract()[1]
                yield Gazette(
                    date=gazette_date,
                    file_urls=[
                        gazette_url_extra,
                    ],
                    edition_number=edition_number,
                    is_extra_edition=True,
                    power="executive_legislative",
                )
            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )
        next_page_url = response.css(".table-pagination .next a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))
