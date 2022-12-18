from dateutil.rrule import DAILY, rrule
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DionetGazetteSpider(BaseGazetteSpider):
    """
    Base Spider for all cities using IONEWS' DIONET product

    In addition to the normal spider attributes, for this base spider
    we must define three other class attributes:

        - json_list_url
            A template string with three fields:
                - year
                - month
                - day
        - gazette_id_url
            A template string with one field:
                - gazette_id
        - power
            A str with the gazette power. Default value: "executive"
    """

    json_list_url = ""
    gazette_id_url = ""
    power = "executive"

    def start_requests(self):
        for date_ in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            day = str(date_.day).zfill(2)
            month = str(date_.month).zfill(2)
            url = self.json_list_url.format(
                year=date_.year,
                month=month,
                day=day,
            )
            yield Request(url=url, cb_kwargs={"gazette_date": date_.date()})

    def parse(self, response, gazette_date):
        gazette_data = response.json()
        if gazette_data["erro"]:
            return

        items = gazette_data.get("itens", [])
        for item in items:
            gazette_id = item["id"]
            gazette_url = self.gazette_id_url.format(gazette_id=gazette_id)
            is_extra_edition = item["suplemento"] == 1
            yield Gazette(
                date=gazette_date,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power=self.power,
            )
