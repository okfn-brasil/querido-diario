from datetime import datetime

from dateparser import parse
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaFeiraDeSantanaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2910800"
    name = "ba_feira_de_santana"
    allowed_domains = ["diariooficial.feiradesantana.ba.gov.br"]
    start_urls = ["http://www.diariooficial.feiradesantana.ba.gov.br"]
    powers = {"executive": 1, "legislative": 2}
    last_page = 1
    handle_httpstatus_list = [302]

    def parse(self, response):
        gazette_table = response.css(".style166")
        gazettes_links = gazette_table.xpath("a//@href").extract()
        dates = gazette_table.css("a::text").extract()

        found_date_by_power = response.meta.get("found_date_by_power", {})

        for url, gazette_date in zip(gazettes_links, dates):
            date_obj = datetime.strptime(gazette_date, "%d/%m/%Y")
            if date_obj.date() >= self.start_date:
                edition = self.extract_edition(url)
                power = self.extract_power(url)
                power_id = self.powers[power]

                if date_obj.date() == self.start_date:
                    found_date_by_power[power] = date_obj.date()

                file_url = response.urljoin(f"abrir.asp?edi={edition}&p={power_id}")
                gazette = Gazette(
                    date=parse(gazette_date, languages=["pt"]).date(),
                    is_extra_edition=False,  # FIXME
                    power=power,
                    edition_number=edition,
                )

                yield Request(
                    file_url,
                    callback=self.parse_document_url,
                    meta={"gazette": gazette},
                )

        # we check the next page because editions from different powers may not be on the same page
        if len(found_date_by_power) < 2:
            current_page_selector = "#pages ul li.current::text"
            current_page = response.css(current_page_selector).extract_first()
            if current_page:
                next_page = int(current_page) + 1
                next_page_url = response.urljoin(f"/?p={next_page}")

                if next_page > self.last_page:
                    self.last_page = next_page
                    yield Request(
                        next_page_url, meta={"found_date_by_power": found_date_by_power}
                    )

    def parse_document_url(self, response):
        gazette = response.meta["gazette"]
        pdf_url = response.headers["Location"].decode("utf-8")
        if pdf_url is None:
            self.logger.error(f"Unable to retrieve PDF URL for {gazette['date']}.")

        gazette["file_urls"] = [pdf_url]
        return gazette

    @staticmethod
    def extract_power(url):
        return "executive" if url.find("st=1") != -1 else "legislative"

    @staticmethod
    def extract_edition(url):
        edition_index = url.find("edicao=") + len("edicao=")
        return url[edition_index:]
