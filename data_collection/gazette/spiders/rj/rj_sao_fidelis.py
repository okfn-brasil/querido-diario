from datetime import datetime as dt

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjSaoFidelisSpider(BaseGazetteSpider):
    name = "rj_sao_fidelis"
    TERRITORY_ID = "3304805"
    allowed_domains = ["saofidelis.rj.gov.br"]
    start_urls = ["https://saofidelis.rj.gov.br/diariooficial/"]
    start_date = dt(2017, 7, 1).date()

    def parse(self, response):
        year_buttons = response.xpath('//button[contains(@id, "e-n-tab-title")]')

        for button in year_buttons:
            year_container_id = button.xpath("./@aria-controls").get()
            year_container = response.xpath(f'//div[@id="{year_container_id}"]')
            accordion_items = year_container.xpath(
                './/details[contains(@class,"e-n-accordion-item")]'
            )

            for accordion in accordion_items:
                paragraphs = accordion.xpath(
                    './/div[contains(@class,"elementor-widget-text-editor")]//p'
                )

                for p in paragraphs:
                    date_str = p.xpath("text()[1]").re_first(r"(\d{2} de \w+ de \d{4})")
                    if not date_str:
                        continue

                    gazette_date = dateparser.parse(
                        date_str.strip(), languages=["pt"]
                    ).date()
                    if gazette_date > self.end_date:
                        continue

                    if gazette_date < self.start_date:
                        return

                    edition = p.xpath(
                        './/strong[contains(text(),"Edição")]/text()'
                    ).re_first(r"Edição\s*(\d+[.\d]*)")
                    gazette_url = p.xpath(
                        './/a[contains(text(),"Download")]/@href'
                    ).get()

                    if gazette_url:
                        gazette_url = response.urljoin(gazette_url)

                        yield Gazette(
                            date=gazette_date,
                            edition_number=edition,
                            is_extra_edition=False,
                            file_urls=[gazette_url],
                            power="executive",
                        )
