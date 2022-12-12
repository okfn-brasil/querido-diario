from datetime import date, datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaAltamiraSpider(BaseGazetteSpider):
    TERRITORY_ID = "1500602"
    allowed_domains = ["altamira.pa.gov.br"]
    name = "pa_altamira"
    start_urls = ["https://altamira.pa.gov.br/diario-oficial"]
    start_date = date(2020, 1, 1)

    def parse(self, response):
        gazettes = response.css(".post-content li")

        for gazette in gazettes:
            title = gazette.css("a::attr(title)").get()
            url = gazette.css("a::attr(href)").get()
            str_date = gazette.css("a::attr(title)").re(r"\d+\/\d+/\d+")
            date = datetime.strptime(str_date, "%d/%m/%Y")
            edition_number = (
                gazette.css("a::attr(title)").re(r"Nº \d+")[0].split(" ")[1]
            )

            if ".pdf" in url:
                yield Gazette(
                    edition_number=edition_number,
                    date=date,
                    file_urls=[url],
                    is_extra_edition="extra" in title.lower(),
                    power="executive_legislative",
                )
            else:
                yield response.follow(url, self.parse_gazette)

    def parse_gazette(self, response):
        gazette = response.css("h3 a")
        edition_number = gazette.re(r"Nº \d+")[0].split(" ")[0]
        url = gazette.css("a::attr(href)").get()
        str_date = gazette.re(r"\d+\/\d+/\d+")
        date = datetime.strptime(str_date, "%d/%m/%Y").date()
        title = gazette("::text").get()

        yield Gazette(
            edition_number=edition_number,
            date=date,
            file_urls=[url],
            is_extra_edition="extra" in title.lower(),
            power="executive_legislative",
        )
