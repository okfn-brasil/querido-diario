from dateutil.rrule import DAILY, rrule
from dateutil.parser import parse
from datetime import date
import requests
from scrapy.selector import Selector
import scrapy
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSaoJoseDosBasiliosSpider(BaseGazetteSpider):
    TERRITORY_ID = "2111250"
    name = "ma_sao_jose_dos_basilios_2023"
    start_date = date(2018, 2, 19)
    end_data = date.today()
    allowed_domains = ["http://diariooficial.saojosedosbasilios.ma.gov.br"]

    def start_requests(self):
        dates = rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date)
        for dt in dates:
            html = requests.get(f"https://diariooficial.saojosedosbasilios.ma.gov.br/diariooficial/edicoes?data_inicial={dt.day}%2F{dt.month}%2F{dt.year}&t=titulo&page=1").text
            response = Selector(text=html)
            pages = []
            for links in response.css(".page-link::text").getall():
                pages.append(links)
            for page in range(1, int(len(pages)-1)):
                yield scrapy.Request(
                    f"https://diariooficial.saojosedosbasilios.ma.gov.br/diariooficial/edicoes?data_inicial={dt.day}%2F{dt.month}%2F{dt.year}&t=titulo&page={page}"
                )

    def parse(self, response):

        editions = response.css(".col-md-12.list-publicacoes-diario a")
        for edition in editions:
            url = response.urljoin(edition.css("a::attr('href')").get())[:80]
            title = edition.css('li h6::text').get().strip().lower()
            date = parse(edition.css("a li::text").getall()[-1].split()[-1]).date()


            yield Gazette(
                            date=date,
                            file_urls=[url],
                            is_extra_edition=True,
                            power="executive",
                        )
