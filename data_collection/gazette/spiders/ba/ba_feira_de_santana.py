from datetime import date, datetime

from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class BaFeiraDeSantanaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2910800"
    name = "ba_feira_de_santana"
    start_date = date(2015, 1, 1)
    allowed_domains = ["diariooficial.feiradesantana.ba.gov.br"]
    start_urls = ["https://www.diariooficial.feiradesantana.ba.gov.br"]
    powers = {"executive": 1, "legislative": 2}
    last_page = 1
    handle_httpstatus_list = [302]

    def parse(self, response):
        gazette_table = response.xpath('//ancestor::tr[td[@class="style166"]]')
        gazettes_links = gazette_table.css("a.link_menu2::attr(href)").getall()
        dates = gazette_table.css("a.link_menu2::text").getall()
        is_extra_flags = gazette_table.xpath("td/div/a/img")

        go_to_next_page = False

        for url, gazette_date, is_extra_edition in zip(
            gazettes_links, dates, is_extra_flags
        ):
            date_obj = datetime.strptime(gazette_date, "%d/%m/%Y")

            if self.start_date <= date_obj.date() <= self.end_date:
                # we check the next page because editions from different powers may not be on the same page
                go_to_next_page = True

                edition = self.extract_edition(url)
                power = self.extract_power(url)
                power_id = self.powers[power]

                file_url = response.urljoin(f"abrir.asp?edi={edition}&p={power_id}")
                is_extra_edition = bool(is_extra_edition.css('[alt$="EXTRA"]').getall())

                gazette = Gazette(
                    date=get_date_from_text(gazette_date),
                    is_extra_edition=is_extra_edition,
                    power=power,
                    edition_number=edition,
                )
                yield Request(
                    file_url,
                    callback=self.parse_document_url,
                    meta={"gazette": gazette},
                )

        if go_to_next_page:
            current_page_selector = "#pages ul li.current::text"
            current_page = response.css(current_page_selector).get()
            if current_page:
                next_page = int(current_page) + 1
                next_page_url = response.urljoin(f"/?p={next_page}")

                if next_page > self.last_page:
                    self.last_page = next_page
                    yield Request(next_page_url)

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
