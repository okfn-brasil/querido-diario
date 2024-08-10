from datetime import date, datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class UFMunicipioSpider(BaseGazetteSpider):
    name = "rj_saquarema"
    TERRITORY_ID = "3305505"
    allowed_domains = ["saquarema.rj.gov.br"]
    start_urls = ["https://dos.saquarema.rj.gov.br/arquivo/"]
    start_date = date(18, 10, 9)

    def parse(self, response):
        for tr in response.xpath("//tbody/tr"):
            raw_gazette_date = tr.xpath("./td/text()")[-1].get()[0:10]
            gazette_date = dt.strptime(raw_gazette_date, "%Y-%m-%d").date()
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            raw_gazette_edition = tr.xpath("./td/text()")[0].get()
            gazette_edition_number = raw_gazette_edition.split("/")[0]
            is_extra_edition = "EXTRA" in raw_gazette_edition.upper()

            gazette_url = tr.xpath(".//a/@href").get()
            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )
