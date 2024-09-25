from datetime import date, datetime
from urllib.parse import parse_qsl, urlencode, urlparse

from scrapy.http import HtmlResponse, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpCacapavaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3508504"
    name = "sp_cacapava"
    allowed_domains = ["cacapava.sp.gov.br", "ecrie.com.br"]
    start_date = date(2021, 4, 27)
    custom_settings = {"DOWNLOAD_DELAY": 0.5, "RANDOMIZE_DOWNLOAD_DELAY": True}

    def start_requests(self):
        data_de = self.start_date.strftime("%d/%m/%Y")
        data_ate = self.end_date.strftime("%d/%m/%Y")
        url = f"https://cacapava.sp.gov.br/diario-oficial?dataDe={data_de}&dataAte={data_ate}"
        yield Request(url)

    def pagination_url(self, url: str, page: str):
        url_parsed = urlparse(url)
        url_query = dict(parse_qsl(url_parsed.query))
        url_query.update({"pagina": page})
        return url_parsed._replace(query=urlencode(url_query)).geturl()

    def parse(self, response: HtmlResponse):
        for gazette in response.css(".list-item__info"):
            edition_number = gazette.css("h3::text").re_first(r"Edição nº (\d+)")
            gazette_raw_date = gazette.css("p::text").re_first(r"\d{2}/\d{2}/\d{4}")
            gazette_date = datetime.strptime(gazette_raw_date, "%d/%m/%Y").date()
            gazette_url = gazette.css("a::attr(href)").get()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
                file_urls=[gazette_url],
            )

        pages = response.css(".pagination__select option::text").getall()
        for page in pages[1:]:
            yield Request(self.pagination_url(response.url, page))
