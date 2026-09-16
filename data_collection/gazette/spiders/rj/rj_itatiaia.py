import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjItatiaiaSpider(BaseGazetteSpider):
    name = "rj_itatiaia"
    TERRITORY_ID = "3302254"
    allowed_domains = ["itatiaia.rj.gov.br"]
    start_date = date(2019, 1, 28)
    BASE_URL = "https://itatiaia.rj.gov.br/wp-admin/admin-ajax.php"

    payload = {
        "action": "jet_smart_filters",
        "provider": "jet-engine/default",
        "defaults[post_status][]": "publish",
        "defaults[post_type]": "boletim-",
        "defaults[posts_per_page]": "50",
        "defaults[paged]": "1",
        "defaults[ignore_sticky_posts]": "1",
        "settings[lisitng_id]": "32705",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    def start_requests(self):
        query_date = f"{self.start_date.strftime('%Y.%m.%d')}-{self.end_date.strftime('%Y.%m.%d')}"
        self.payload["query[_date_query_|date]"] = query_date
        yield scrapy.FormRequest(
            url=self.BASE_URL, headers=self.headers, formdata=self.payload
        )

    def parse(self, response):
        content = response.json()["content"]
        gazette_list = content.split("\n\t\t\t\t\t\t\t\t")
        for i in range(2, len(gazette_list), 2):
            gazette_data = gazette_list[i]

            date_match = re.search(r"<h6.*?>(.*?)</h6>", gazette_data).group(1)
            gazette_date = dt.strptime(date_match, "%d/%m/%Y").date()

            title_match = re.search(r"<h5.*?>(.*?)</h5>", gazette_data)
            title_match = title_match.group(1).lower()
            extra = "extra" in title_match

            url_match = re.search(r'href="(.*?)"', gazette_data).group(1)

            edition_match = re.search(r"nº (\d+)", title_match).group(1)

            yield Gazette(
                date=gazette_date,
                edition_number=edition_match,
                is_extra_edition=extra,
                file_urls=[url_match],
                power="executive_legislative",
            )

        pagination = response.json()["pagination"]
        page = pagination["page"]
        last_page = pagination["max_num_pages"]
        self.payload["defaults[paged]"] = str(int(self.payload["defaults[paged]"]) + 1)
        if page < last_page:
            yield scrapy.FormRequest(
                url=self.BASE_URL, headers=self.headers, formdata=self.payload
            )
