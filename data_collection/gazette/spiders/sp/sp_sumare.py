import re
from datetime import date, datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSumareSpider(BaseGazetteSpider):
    TERRITORY_ID = "3552403"
    allowed_domains = ["sumare.sp.gov.br"]
    name = "sp_sumare"
    start_urls = ["https://www.sumare.sp.gov.br/Diario.Oficial.php?edicao=todas"]
    start_date = date(2011, 2, 11)

    def parse(self, response):
        gazettes = response.css("li.umDO")

        for gazette in gazettes:
            title = gazette.css(".file-title::text").get()
            url = gazette.css("a::attr(href)").get()
            str_date = gazette.css(".areaMetade::text").get()
            date = datetime.strptime(str_date, "%d/%m/%Y").date()

            if not (self.start_date <= date <= self.end_date):
                continue

            yield Gazette(
                edition_number=re.search(r"\d+", title.strip()).group(0),
                date=date,
                file_urls=[response.urljoin(url)],
                is_extra_edition="extra" in title.lower(),
                power="executive_legislative",
            )
