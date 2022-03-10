from datetime import date

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeJaboataoDosGuararapesSpider(BaseGazetteSpider):
    TERRITORY_ID = "2607901"
    name = "pe_jaboatao_dos_guararapes"
    allowed_domains = ["diariooficial.jaboatao.pe.gov.br"]
    start_urls = ["https://diariooficial.jaboatao.pe.gov.br/"]
    start_date = date(2015, 10, 3)
    end_date = date.today()

    def parse(self, response):
        for gazette_card in response.css(".elementor-post__card"):
            gazette_date = parse(
                gazette_card.css(".elementor-post-date::text").get(),
            ).date()

            if gazette_date < self.start_date:
                return
            elif gazette_date > self.end_date:
                continue
            else:
                yield Request(
                    gazette_card.css(".elementor-post__title a::attr(href)").get(),
                    callback=self.parse_gazette_page,
                    cb_kwargs={"gazette_date": gazette_date},
                )

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page)

    def parse_gazette_page(self, response, gazette_date):
        pdf_link = response.css(".dkpdf-button::attr(href)").get()
        file_url = response.urljoin(pdf_link)

        return Gazette(
            date=gazette_date,
            file_urls=[file_url],
            is_extra_edition="edicao-extraordinaria" in file_url,
            power="executive",
        )
