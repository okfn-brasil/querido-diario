import re
from datetime import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSumareSpider(BaseGazetteSpider):
    TERRITORY_ID = "3552403"
    allowed_domains = ["https://www.sumare.sp.gov.br"]
    name = "sp_sumare"
    start_urls = ["https://www.sumare.sp.gov.br/Diario.Oficial.php?edicao=todas"]
    base_url = "https://www.sumare.sp.gov.br/"

    def parse(self, response):
        gazettes = response.css("li.umDO")
        gazettes.reverse()

        for gazette in gazettes:
            title = gazette.css("a::attr(title)").get()
            url = gazette.css("a::attr(href)").get()
            str_date = re.search(r"\d+/\d+/\d{4}", title).group(0)
            date = datetime.strptime(str_date, "%d/%m/%Y").date()

            if hasattr(self, "start_date") and date < self.start_date:
                continue

            gazette_data = {
                "edition_number": re.search(r"\d+", title).group(0),
                "date": date,
                "file_urls": [f"{self.base_url}{url}"],
                "is_extra_edition": "extra" in title.lower(),
                "power": "executive",
            }

            yield Gazette(
                **gazette_data,
                scraped_at=datetime.utcnow(),
            )
