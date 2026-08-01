from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjArraialdoCaboSpider(BaseGazetteSpider):
    TERRITORY_ID = "3300258"
    name = "rj_arraial_do_cabo"
    allowed_domains = ["portal.arraial.rj.gov.br"]
    start_urls = ["https://portal.arraial.rj.gov.br/diarios_oficiais_web"]
    start_date = date(2019, 4, 11)

    def parse(self, response):
        for entry in response.css(".row .card.card-margin"):
            edition = entry.css("h5.card-title").re_first(r"(\d*) \/ \d{4}")
            file_url = entry.css(".widget-49-meeting-action.mt-2 a::attr(href)").get()
            publish_date = entry.css(".widget-49-date-day::text").get()
            publish_date = datetime.strptime(publish_date, "%d %b %Y").date()

            if self.start_date <= publish_date <= self.end_date:
                yield Gazette(
                    date=publish_date,
                    file_urls=[file_url],
                    edition_number=edition,
                    is_extra_edition=False,
                    power="executive",
                )

        next_page = response.xpath('//a[contains(@rel, "next")]/@href')[-1]
        if next_page and publish_date > self.start_date:
            yield Request(next_page.get())
