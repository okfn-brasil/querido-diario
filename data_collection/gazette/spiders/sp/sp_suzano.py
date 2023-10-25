import datetime
import re

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSuzanoSpider(BaseGazetteSpider):
    name = "sp_suzano"
    TERRITORY_ID = "3552502"
    start_date = datetime.date(2017, 8, 1)
    start_urls = ["https://suzano.sp.gov.br/web/transparencia/imprensa-oficial/"]

    def parse(self, response):
        info = response.xpath("/html/body/div[2]/div/div/div[2]/div/div/*/*/span[2]")
        data = response.xpath(
            "/html/body/div[2]/div/div/div[2]/div/div/*/div[@class='desc']"
        )
        file_pattern = r'href="(https://[^"]+\.pdf)"'
        date_pattern = r"(\d{1,2}[./]\d{1,2}[./]\d{4})"
        for index, element in enumerate(data):
            title = info[index].get()
            matches_url = re.findall(file_pattern, element.get())
            matches_date = re.findall(date_pattern, title)
            if matches_url and matches_date:
                url = matches_url[0]
                if "/" in matches_date[0]:
                    date = datetime.datetime.strptime(
                        matches_date[0], "%d/%m/%Y"
                    ).date()
                else:
                    date = datetime.datetime.strptime(
                        matches_date[0], "%d.%m.%Y"
                    ).date()
                is_extra = True if (title.find("Extra") != -1) else False

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra,
                    power="executive",
                )
