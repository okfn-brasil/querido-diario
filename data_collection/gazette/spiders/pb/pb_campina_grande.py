from dateutil.parser import parse
from dateutil.rrule import MONTHLY, rrule
import scrapy
from datetime import date
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbCampinaGrandeSpiderExecutive(BaseGazetteSpider):
    TERRITORY_ID = "2504009"
    allowed_domains = ["campinagrande.pb.gov.br"]
    name = "pb_campina_grande"
    start_date = date(2017, 1, 1)

    def start_requests(self):
        dates = rrule(freq=MONTHLY, dtstart=self.start_date, until=date.today())
        for date_url in dates:
            for page in range(1,4):
                yield scrapy.Request(
                    f"https://campinagrande.pb.gov.br/semanario-oficial/semanario-oficial-{date_url.year}/page/{page}/?mes={date_url.month}",
                )

    def parse(self, response):
        months_urls = response.css(".component-archiveFiles .info a::attr(href)").getall()
        yield from response.follow_all(months_urls, self.parse_month)

    def parse_month(self, response):
        editions = response.css(".main_single__content")
        if not editions:
            self.logger.debug(f"No editions found at {response.url}")
        else:
            for edition in editions:
                urls_editions = edition.css(".main-content-single a::attr(href)").getall()
                date_tmp = edition.css("div:nth-child(4) > p > strong::text").get()
                date_edition = parse('/'.join(date_tmp.split()[0].split('/')[::-1])).date()
                title_edition = response.css("h1.single_title::text").get().replace("\n","").lower()
                
                yield Gazette(
                    date=date_edition,
                    file_urls=urls_editions,
                    is_extra_edition="separata" in title_edition,
                    power="executive",
                )
