import json
import time
from dateparser import parse
from datetime import datetime
from scrapy import Request
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# based on the website
FIRST_YEAR = 1967
BASE_URL = "https://diariooficial.cuiaba.mt.gov.br/api/api/editions"


# class TooManyRequestsRetryMiddleware(RetryMiddleware):
#     def __init__(self, crawler):
#         super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
#         self.crawler = crawler

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler)

#     def process_response(self, request, response, spider):
#         if response.status == 429:
#             delay = int(response.headers.get("Retry-After", 25))
#             self.crawler.engine.pause()
#             time.sleep(delay)
#             self.crawler.engine.unpause()
#             return self._retry(request, "429 response", spider) or response
#         return response


class MtCuiabaSpider(BaseGazetteSpider):
    TERRITORY_ID = 5103403
    name = "mt_cuiaba"
    allowed_domains = ["diariooficial.cuiaba.mt.gov.br"]
    start_urls = ["https://diariooficial.cuiaba.mt.gov.br/"]

    # handle_httpstatus_list = [429]

    custom_settings = {
        # "RETRY_TIMES": 5,
        "CONCURRENT_REQUESTS": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "DOWNLOAD_DELAY": 1,
        # "DOWNLOADER_MIDDLEWARES":{
        #     "gazette.spiders.mt_cuiaba.TooManyRequestsRetryMiddleware": 98
        # },
    }

    def start_requests(self):
        today = datetime.today()
        final_year = today.year
        for year in range(FIRST_YEAR, final_year + 1):
            for month in range(1, 13):
                date_url = f"{BASE_URL}/published/{year}/{month}"
                yield Request(
                    url=date_url,
                    headers={
                        "referer": "https://diariooficial.cuiaba.mt.gov.br/edicoes",
                    }
                )

    def parse(self, response):
        # if response.status == 429:
        #     delay = int(response.headers.get("Retry-After", 25))
        #     self.crawler.stats.inc_value("response_429")
        #     print(f"Got response 429, start waiting {delay} seconds...")
        #     time.sleep(delay)
        #     yield Request(
        #         response.url,
        #         dont_filter=True,
        #     )
        editions = json.loads(response.text)["editions"]
        for edition in editions:
            edition_id = edition["id"]
            edition_url = f"{BASE_URL}/downloadPdf/{edition_id}"
            edition_date = edition["publication_date"]

            yield Gazette(
                date=parse(edition_date, languages=["pt"]),
                file_urls=[edition_url],
                is_extra_edition=edition["suplement"],
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.utcnow(),
            )
