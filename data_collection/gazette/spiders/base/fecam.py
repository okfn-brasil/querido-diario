import re
from urllib.parse import parse_qs, urlparse

from dateutil.rrule import DAILY, rrule, rruleset
from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseFecamSpider(BaseGazetteSpider):
    allowed_domains = ["diariomunicipal.sc.gov.br", "dom.sc.gov.br"]
    code = None

    def start_requests(self):
        daily_dates = rruleset()
        daily_dates.rrule(rrule(DAILY, dtstart=self.start_date, until=self.end_date))

        query = parse_qs(self.GAZETTES_PAGE_URL)
        self.code = query.get("codigoEntidade")[0]

        for day in daily_dates:
            yield self._requests(
                day=day.date(),
                page=1,
                callback=self.request_all_pages,
            )

    def request_all_pages(self, response, day):
        if "pagination" in response.text:
            last_page_raw = response.css(".last")[0].css("a::attr(href)").get()
            last_page_number = int(re.search(r"page=(\d*)", last_page_raw).group(1))

            # page 1 already requested by default in start_requests
            for page in range(2, last_page_number + 1):
                yield self._requests(day=day, page=page, callback=self.parse_page)

        # response contains page 1 items and needs to be parsed
        self.parse_page(response, day)

    def parse_page(self, response, day):
        for item in response.css(".span5 .quiet"):
            act_url = self._fix_url(item.xpath("following-sibling::a[1]/@href").get())
            act_infos = "".join(item.css("::text").getall()).split(" - ")

            yield Gazette(
                date=day,
                power=self.POWER,
                edition_number="",
                is_extra_edition=False,
                granularity="ato",
                act_category=act_infos[-2],
                publishing_body=act_infos[-1],
                document_code="",
                document_page="",
                file_urls=[act_url],
            )

    def _requests(self, day, page, callback):
        formdata = {
            "r": "pesquisa/entidade",
            "id": self.code,
            "data": day.strftime("%Y-%m-%d"),
            "AtoASolrDocument_page": str(page),
        }
        return FormRequest(
            url="https://www.diariomunicipal.sc.gov.br/?",
            method="GET",
            formdata=formdata,
            callback=callback,
            cb_kwargs={"day": day},
        )

    def _fix_url(self, url):
        # some file_url has relative path only, instead of full path
        netloc = self.allowed_domains[0]
        if netloc not in url:
            return urlparse(url)._replace(scheme="https", netloc=netloc).geturl()
        return url
