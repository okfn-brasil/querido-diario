import re
from datetime import datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjVoltaRedondaSpider(BaseGazetteSpider):
    name = "rj_volta_redonda"
    TERRITORY_ID = "3306305"
    allowed_domains = ["voltaredonda.rj.gov.br"]
    start_urls = ["https://www.voltaredonda.rj.gov.br/vrdestaque/index.php"]
    start_date = dt(2019, 1, 4).date()

    def parse(self, response):
        gazettes = response.xpath('//select[@id="search"]/option[@value]')
        gazettes.reverse()

        for gazette in gazettes:
            gazette_url = gazette.xpath("@value").get()

            match = re.search(
                r"(?<!\d)(?P<year>20[0-9]{2})-(?P<month>0[1-9]|1[0-2])-(?P<day>0[1-9]|[1-2][0-9]|3[0-1])(?!\d)",
                gazette_url,
            )
            if not match:
                continue

            gazette_date = dt.strptime(match.group(), "%Y-%m-%d").date()

            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            title = gazette.xpath("text()").get().strip()
            is_extra = "EXTRA" in title.upper()

            gazette_edition_number = re.search(r"\d+", title).group()

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra,
                file_urls=[response.urljoin(gazette_url)],
                power="executive_legislative",
            )
