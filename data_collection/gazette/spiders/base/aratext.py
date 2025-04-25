import re
from urllib.parse import urlparse

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class BaseAratextSpider(BaseGazetteSpider):
    def parse(self, response, page=1):
        for item in response.css("#edicoes-anteriores tbody tr"):
            raw_edition_date = (
                item.css("td")[2].css("::text").get().split(",")[1].strip()
            )
            edition_date = get_date_from_text(raw_edition_date)

            raw_edition_number = item.css("a::text").get().strip()
            edition_number = re.search(r"N.? (.*)/", raw_edition_number).group(1)

            path = item.css("a").attrib["href"]
            intermediary_page = (
                urlparse(self.start_urls[0])._replace(path=path).geturl()
            )
            if self.start_date <= edition_date <= self.end_date:
                gazette = {
                    "date": edition_date,
                    "edition_number": edition_number,
                    "is_extra_edition": False,
                    "power": self.power,
                }

                yield Request(
                    intermediary_page,
                    callback=self.parse_intermediary_page,
                    cb_kwargs={"gazette": gazette},
                )

        last_page = response.xpath('//*[@class="pagination"]//*[@rel="next"]') == []

        if edition_date > self.start_date and not last_page:
            page += 1
            yield Request(
                f"{self.start_urls[0]}?page={page}",
                callback=self.parse,
                cb_kwargs={"page": page},
            )

    def parse_intermediary_page(self, response, gazette):
        file_path = response.css("#Box-area-title a").attrib["href"]
        gazette_url = urlparse(self.start_urls[0])._replace(path=file_path).geturl()

        yield Gazette(**gazette, file_urls=[gazette_url])
