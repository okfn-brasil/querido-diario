from datetime import date
from urllib.parse import urlencode

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsLajeadoSpider(BaseGazetteSpider):
    TERRITORY_ID = "4311403"
    BASE_URL = "https://lajeado.rs.gov.br"

    name = "rs_lajeado"
    start_date = date(2016, 4, 5)
    params = {
        "titulo": "Diário Oficial",
        "template": "conteudo",
        "codigoCategoria": 1012,
    }

    def start_requests(self):
        params = urlencode(self.params)
        yield Request(self.BASE_URL + "/?" + params)

    def parse(self, response):
        pdfs = response.css("ul.anexos li a")
        for item in pdfs:
            filename = item.css("::text").get()

            kwargs = {"filedate": self.extract_date(filename)}

            href = item.attrib["href"]
            href = response.urljoin(href)

            yield Request(href, method="GET", callback=self.parse_url, cb_kwargs=kwargs)

    def parse_url(self, response, **kwargs: dict):
        url = response.css("div.topoAbreAnexoDownload a::attr(href)").get()
        yield Gazette(
            date=kwargs["filedate"],
            file_urls=[url],
            power="legislative",
            territory_id=self.TERRITORY_ID,
        )

    @staticmethod
    def extract_date(filename: str) -> date:
        filedate, *_ = filename.split("_")

        # There is a single case where the first day
        # of the month is represented like '1º'
        filedate = filedate.replace("º", "")

        filedate = filedate.split("/")

        # There is a single case where the date is formatted
        # as 'dd mm yy' instead of 'dd/mm/yy'
        if len(filedate) == 1:
            filedate = filedate[0].split()

        day, month, year = (int(f) for f in filedate)
        return date(year + 2000, month, day)
