import re
from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class RjBomJardimSpider(BaseGazetteSpider):
    name = "rj_bom_jardim"
    TERRITORY_ID = "3300506"
    allowed_domains = ["diario-oficial.online"]
    start_urls = ["https://diario-oficial.online/publicacoes/todas/1?page=1"]
    start_date = date(2023, 2, 15)

    def parse(self, response):
        data = response.css("div.col-lg-4")
        for item in data:
            edition_number = item.css("h5::text").get().strip()
            extra_edition = "extra" in edition_number.lower()
            edition_number = re.sub(r"\D", "", edition_number)

            raw_edition_date = (
                item.css('span[style="font-size: 12px;"]::text').get().strip()
            )
            edition_date = get_date_from_text(raw_edition_date)

            if edition_date > self.end_date:
                continue
            if edition_date < self.start_date:
                return

            edition_url = item.css("div.option-box a::attr(href)").get()
            edition_url = response.urljoin(edition_url)

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                is_extra_edition=extra_edition,
                file_urls=[edition_url],
                power="executive",
            )

        next_page = response.css('a[aria-label="Próxima"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
