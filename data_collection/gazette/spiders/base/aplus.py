import datetime as dt
import re

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAplusSpider(BaseGazetteSpider):
    def start_requests(self):
        start_date = self.start_date.strftime("%Y/%m/%d")
        end_date = self.end_date.strftime("%Y/%m/%d")
        yield FormRequest(
            url=self.url_base,
            formdata={"data": start_date, "data2": end_date, "termo": "", "submit": ""},
        )

    def parse(self, response):
        gazettes = response.xpath("//tbody/tr")

        for gazette in gazettes:

            gazette_date = dt.datetime.strptime(
                gazette.xpath("./td[2]/text()").get(), "%d/%m/%Y"
            ).date()

            edition_number = gazette.xpath("./td[1]/text()").get()
            hyphenated_suffix = re.search(r"-\d+$", edition_number)
            is_extra_edition = True if hyphenated_suffix is not None else False
            gazette_url = gazette.css("td a::attr(href)").get()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
