from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class BaseDionetSpider(BaseGazetteSpider):
    """
    Base Spider for all cities using IONEWS' DIONET product

    In addition to the normal spider attributes, for this base spider
    one other class attributes may be necessary:
        - subtheme
    """

    url_subtheme = ""

    def start_requests(self):
        for date in daily_sequence(self.start_date, self.end_date):
            api_path = f"/apifront/portal/edicoes/edicoes_from_data/{date.strftime('%Y-%m-%d')}.json"
            url = "".join([self.BASE_URL, api_path, self.url_subtheme])

            yield Request(url=url, cb_kwargs={"gazette_date": date.date()})

    def parse(self, response, gazette_date):
        gazette_data = response.json()
        if gazette_data["erro"]:
            return

        items = gazette_data.get("itens", [])
        for item in items:
            gazette_id = item["id"]
            gazette_url = f"{self.BASE_URL}/portal/edicoes/download/{gazette_id}"

            is_extra_edition = item["suplemento"] == 1
            edition_number = item["numero"]

            yield Gazette(
                date=gazette_date,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power="executive",
            )
