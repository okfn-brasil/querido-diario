import datetime

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnPauDosFerrosSpider(BaseGazetteSpider):
    name = "rn_pau_dos_ferros_2017"
    allowed_domains = ["paudosferros.rn.gov.br"]
    start_date = datetime.date(2017, 1, 2)
    end_date = datetime.date(2022, 9, 28)
    TERRITORY_ID = "2409407"
    start_urls = ["https://paudosferros.rn.gov.br/publicacoes.php?grupo=&cat=11"]

    def parse(self, response, page=1):
        gazettes = response.css(".list-group-item")
        last_page_number_css = ".pagination > li:nth-last-child(-n+2) > a > span::text"
        last_page_number = int(response.css(last_page_number_css).get())
        follow_next_page = True

        for gazette in gazettes:
            gazette_date_raw = gazette.css("div > div > span::text").get().strip()
            gazette_date = parse(gazette_date_raw, languages=["pt"]).date()

            gazette_title_raw = gazette.css("h4 > div > div > strong::text").get()

            edition_number = gazette_title_raw.strip()

            if gazette_date < self.start_date or page == last_page_number:
                follow_next_page = False

            partial_url = gazette.css("a::attr(href)").get()
            url = f"https://paudosferros.rn.gov.br/{partial_url}"

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                edition_number=edition_number,
                power="executive_legislative",
            )

        if follow_next_page:
            next_page = page + 1
            yield Request(
                f"{self.start_urls[0]}&pagina={page}",
                cb_kwargs={"page": next_page},
            )
