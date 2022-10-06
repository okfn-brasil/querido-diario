import dateparser
from datetime import date
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgEsmeraldasSpider(BaseGazetteSpider):
    name = "mg_esmeraldas"
    allowed_domains = ["esmeraldas.mg.gov.br"]
    start_date = date(2021, 8, 12)
    url_base = "https://www.esmeraldas.mg.gov.br/diario-oficial-eletronico"
    start_urls = [url_base]
    TERRITORY_ID = "3124104"

    def parse(self, response):
        for row in response.xpath("//table[@class='table table-striped table-diario']/tbody/tr"):
            url = row.xpath("./td/a/@href").get()
            date = row.xpath("./td/a/span/text()").get()
            date = date.replace("\xa0","")
            date = dateparser.parse(date, languages=["pt"]).date()
            edition = row.xpath("./td/a/@title").get()
            is_extra_edition = "EXTRAORDINÁRIA" in edition
            edition_number = edition.split()[1]
            if date >= self.start_date and date <= self.end_date:
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    edition_number=edition_number,
                    is_extra_edition = is_extra_edition,
                    power="executive"
                )
    
