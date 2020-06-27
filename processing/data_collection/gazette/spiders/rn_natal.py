from datetime import datetime

import dateparser
from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnNatalSpider(BaseGazetteSpider):

    name = "rn_natal"
    allowed_domains = ["www.natal.rn.gov.br"]

    def start_requests(self):
        base_url = "http://www.natal.rn.gov.br/dom/"
        for year in range(2003, datetime.now().year + 1):
            for month in range(1, 13):
                data = dict(ano=str(year), mes=str(month).zfill(2), list="Listar")
                yield FormRequest(url=base_url, formdata=data)

    def parse(self, response):
        for entry in response.css("#texto a"):
            file_url = response.urljoin(entry.css("::attr(href)").get())
            title = entry.css("::text").get()
            date = dateparser.parse(title.split("-")[-1], languages=["pt"]).date()
            extra_edition = "Extra" in title

            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=extra_edition,
                territory_id="2408102",
                power="executive",
                scraped_at=datetime.utcnow(),
            )
