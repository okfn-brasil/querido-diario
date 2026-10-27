from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class BaseGovWebSpider(BaseGazetteSpider):
    """Base spider for the GovWeb platform, hosted on the city hall website.

    Editions are listed at `{base_url}/diariooficial/pesquisa/...`, filtered by
    publication date, and downloaded from
    `{base_url}/download/diariooficial/edition/{id}`.
    """

    power = "executive"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "base_url"):
            raise NotConfigured("Please set a value for `base_url`")

        self.allowed_domains = [urlparse(self.base_url).netloc]

        super(BaseGovWebSpider, self).__init__(*args, **kwargs)

    async def start(self):
        yield scrapy.Request(self._search_url(1), cb_kwargs={"page": 1})

    def _search_url(self, page):
        # path segments: text search, edition number, start date, end date, page
        return (
            f"{self.base_url}/diariooficial/pesquisa/all/all/"
            f"{self.start_date:%Y-%m-%d}/{self.end_date:%Y-%m-%d}/{page}"
        )

    def parse(self, response, page):
        # innermost blocks holding both the edition title and its view link
        editions = response.xpath(
            "//div[.//h3][.//a[contains(@href, '/diariooficial/view/')]]"
            "[not(.//div[.//h3][.//a[contains(@href, '/diariooficial/view/')]])]"
        )
        for edition in editions:
            raw_date = edition.css("h3 + p::text").get("").split(",")[-1]
            edition_date = get_date_from_text(raw_date)
            if edition_date is None or not (
                self.start_date <= edition_date <= self.end_date
            ):
                continue

            edition_number = edition.css("h3::text").re_first(r"\d+")
            badges = " ".join(edition.css("span::text").getall()).lower()
            edition_id = (
                edition.css("a[href*='/diariooficial/view/']::attr(href)")
                .get()
                .rstrip("/")
                .split("/")[-1]
            )

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                file_urls=[
                    response.urljoin(f"/download/diariooficial/edition/{edition_id}")
                ],
                is_extra_edition="suplementar" in badges,
                power=self.power,
            )

        # requesting a page beyond the last one returns the first page again, so
        # the number of pages is taken from the paginator
        if page == 1:
            last_page = max(
                map(int, response.css("nav.paginator a::attr(href)").re(r"/(\d+)$")),
                default=1,
            )
            for next_page in range(2, last_page + 1):
                yield scrapy.Request(
                    self._search_url(next_page), cb_kwargs={"page": next_page}
                )
