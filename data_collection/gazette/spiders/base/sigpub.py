import json

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class BaseSigpubSpider(BaseGazetteSpider):
    """www.diariomunicipal.com.br (Sigpub) base spider

    Documents obtained by this kind of spider are text-PDFs with many cities in it.
    That's because the websites are usually made for associations of cities.

    TODO:
        - All variations have a "possible" start date of 01/01/2009, but that may cause
        many unnecessary requests to be made if they actually start making available
        documents later. Some investigation for the start date of each website needs to
        be made in this case.

    Observations:
        - These websites have an "Advanced Search", but they are protected by ReCaptcha.
    """

    allowed_domains = ["diariomunicipal.com.br"]

    def __init__(self, *args, **kwargs):
        super(BaseSigpubSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.GAZETTES_PAGE_URL]

    def parse(self, response):
        """Makes requests for each date to see if a document is available."""
        default_form_fields = {
            "calendar[_token]": response.xpath(
                "//input[@id='calendar__token']/@value"
            ).get()
        }
        for gazette_date, date_form_fields in self.available_dates_form_fields():
            formdata = {**default_form_fields, **date_form_fields}

            yield scrapy.FormRequest(
                url=response.urljoin("materia/calendario"),
                formdata=formdata,
                meta={"date": gazette_date, "edition_type": "regular"},
                callback=self.parse_gazette_info,
            )
            yield scrapy.FormRequest(
                url=response.urljoin("materia/calendario/extra"),
                formdata=formdata,
                meta={"date": gazette_date, "edition_type": "extra"},
                callback=self.parse_gazette_info,
            )

    def parse_gazette_info(self, response):
        """Parses document availability endpoint and gets document URL if available."""
        body = json.loads(response.text)
        meta = response.meta

        if "error" in body:
            self.logger.debug(
                f"{meta['edition_type'].capitalize()} Gazette not available for {meta['date'].date()}"
            )
            return

        for edition in body["edicao"]:
            url = f"{body['url_arquivos']}{edition['link_diario']}.pdf"
            yield Gazette(
                date=meta["date"].date(),
                power="executivo_legislativo",
                edition_number=edition.get("numero_edicao", ""),
                is_extra_edition=(meta["edition_type"] == "extra"),
                granularity="agregado",
                act_category="",
                publishing_body="",
                document_code="",
                document_page="",
                file_urls=[url],
            )

    def available_dates_form_fields(self):
        """Generates dates and corresponding form fields for availability endpoint."""
        for query_date in daily_sequence(self.start_date, self.end_date):
            form_fields = {
                "calendar[day]": str(query_date.day),
                "calendar[month]": str(query_date.month),
                "calendar[year]": str(query_date.year),
            }
            yield query_date, form_fields
