import re
from datetime import date, datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ApSantanaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1600600"
    name = "ap_santana"
    allowed_domains = ["santana.ap.gov.br"]
    start_urls = [
        "https://www.santana.ap.gov.br/wp-admin/admin-ajax.php?action=datatables_endpoint"
    ]

    start_date = date(2019, 1, 8)

    def parse(self, response):
        for gazette in response.json()["data"]:
            gazette_date = datetime.strptime(gazette["data"], "%d/%m/%Y").date()

            if gazette_date < self.start_date or self.end_date < gazette_date:
                continue

            file_html = gazette["arquivo"]
            file_url_match = re.search(r'href=[\'"]?([^\'" >]+)[\'"]>Baixar', file_html)
            if not file_url_match:
                continue

            file_url = file_url_match.group(1)

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    file_url,
                ],
                is_extra_edition=False,
                power="executive",
            )
