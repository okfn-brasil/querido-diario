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
            file_url = self._drive_download_url(file_url)

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    file_url,
                ],
                is_extra_edition=False,
                power="executive",
            )

    def _drive_download_url(self, file_url):
        # Some editions link to the Google Drive viewer instead of the file
        if "drive.google.com" not in file_url:
            return file_url

        file_id_match = re.search(r"/file/d/([\w-]+)|[?&;]id=([\w-]+)", file_url)
        if not file_id_match:
            return file_url

        file_id = file_id_match.group(1) or file_id_match.group(2)
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        resource_key_match = re.search(r"[?&;]resourcekey=([\w-]+)", file_url)
        if resource_key_match:
            download_url += f"&resourcekey={resource_key_match.group(1)}"

        return download_url
