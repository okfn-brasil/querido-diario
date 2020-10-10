import re
import urllib
import datetime as dt

from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    TERRITORY_ID = "2408003"

    GAZETTES_URL_SELECTOR = '.pt-cv-thumb-default::attr("href")'
    GAZETTE_PDF_URL_SELECTOR = 'iframe::attr("src")'
    GAZETTE_URL_REGEXP = (
        r".*\/(?P<date>\d{4}\/\d{2}\/\d{2})\/jom-n-o-(?P<edition_number>[^\/-]+).*"
    )

    allowed_domains = ["prefeiturademossoro.com.br"]
    name = "rn_mossoro"
    start_urls = ["http://jom.prefeiturademossoro.com.br/todas-as-edicoes-2/"]

    def parse(self, response):
        for gazette_url in response.css(self.GAZETTES_URL_SELECTOR).extract():
            yield Request(gazette_url, callback=self.parse_gazette)

        if self.has_next_page(response):
            next_url = self.extract_next_page_url(response.url)
            yield Request(next_url, self.parse)

    def has_next_page(self, response):
        return "Nenhum post encontrado" not in str(response.body)

    def extract_next_page_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed_url.query)
        current_page = int(query.get("_page", [1])[0])
        query["_page"] = current_page + 1

        return urllib.parse.ParseResult(
            scheme=parsed_url.scheme,
            netloc=parsed_url.hostname,
            path=parsed_url.path,
            params=parsed_url.params,
            query=urllib.parse.urlencode(query),
            fragment=parsed_url.fragment,
        ).geturl()

    def parse_gazette(self, response):
        gazette_details_url = response.url
        gazette_pdf_url = self.extract_gazette_pdf_url(response)

        return self.extract_gazette(gazette_details_url, gazette_pdf_url)

    def extract_gazette(self, gazette_details_url, gazette_pdf_url):
        match = re.match(self.GAZETTE_URL_REGEXP, gazette_details_url).groupdict()
        date = dt.datetime.strptime(match["date"], "%Y/%m/%d")
        edition_number = match["edition_number"]
        is_extra_edition = bool(re.compile("[A-Za-z]").search(edition_number))

        return Gazette(
            date=date,
            file_urls=[gazette_pdf_url],
            is_extra_edition=is_extra_edition,
            territory_id=self.TERRITORY_ID,
            power="executive_legislature",
            scraped_at=dt.datetime.utcnow(),
        )

    def extract_gazette_pdf_url(self, element):
        iframe_url = element.css(self.GAZETTE_PDF_URL_SELECTOR).extract_first()
        iframe_url_parsed = urllib.parse.urlparse(iframe_url)
        querystrings = urllib.parse.parse_qs(iframe_url_parsed.query)
        return querystrings["file"][0]
