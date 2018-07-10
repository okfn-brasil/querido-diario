from datetime import date, datetime, timedelta
from functools import partial

from scrapy import Request, Spider

from gazette.items import Gazette


class MgBeloHorizonteSpider(Spider):
    MUNICIPALITY_ID = 3106200
    name = "mg_belo_horizonte"
    allowed_domains = ["portal6.pbh.gov.br"]
    documents_url = (
        "http://portal6.pbh.gov.br/dom/iniciaEdicao.do"
        "?method=DomDia&dia={}&comboAno={}"
    )
    first_edition = date(2002, 3, 21)

    def start_requests(self):
        current_date = date.today()
        while current_date >= self.first_edition:
            formatted_date = current_date.strftime("%d/%m/%Y")
            yield Request(
                self.documents_url.format(formatted_date, current_date.year),
                callback=partial(self.parse_page_link, current_date),
            )
            current_date -= timedelta(days=1)

    def parse_page_link(self, current_date, response):
        xpath = '//p[contains(@class,"dom-chamadas")]/a/@href'
        url_path = response.xpath(xpath).extract_first()
        if url_path:
            yield Request(
                response.urljoin(url_path),
                callback=partial(self.parse_details, current_date),
            )

    def parse_details(self, current_date, response):
        xpath = '//a[contains(@alt, "link_anexo")]/@href'
        file_url = response.xpath(xpath).extract_first()
        if file_url:
            yield Gazette(
                date=current_date,
                file_urls=[response.urljoin(file_url)],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power="executive_legislature",
                scraped_at=datetime.utcnow(),
            )
