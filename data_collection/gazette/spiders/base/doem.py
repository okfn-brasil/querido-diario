import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence
from gazette.utils.extraction import get_date_from_text


class BaseDoemSpider(BaseGazetteSpider):
    """
    Base spider for all cities listed on https://doem.org.br
    """

    allowed_domains = ["doem.org.br"]

    # Must be defined in child class
    state_city_url_part = None
    start_date = None

    custom_settings = {
        "DOWNLOAD_FAIL_ON_DATALOSS": False,
    }

    def start_requests(self):
        for month_year in monthly_sequence(
            self.start_date, self.end_date, format="%Y/%m"
        ):
            yield scrapy.Request(
                f"https://doem.org.br/{self.state_city_url_part}/diarios/{month_year}"
            )

    def parse(self, response):
        """
        Parse each page from the results page and yield the gazette issues available.
        """
        gazette_boxes = response.css("div.box-diario")

        for gazette_box in gazette_boxes:
            file_url = self.get_pdf_url(gazette_box)
            date = self.get_gazette_date(gazette_box)
            edition_number = self.get_edition_number(gazette_box)

            if self.start_date <= date <= self.end_date:
                yield Gazette(
                    date=date,
                    file_urls=[file_url],
                    edition_number=edition_number,
                    is_extra_edition=False,
                    power="executive_legislative",
                )

    def get_pdf_url(self, response_item):
        """
        Gets the url for the gazette inside one of the 'box-diario' divs
        """
        preview_link = response_item.css(
            "a[title='Baixar Publicação']::attr(href)"
        ).get()
        return preview_link.replace("previsualizar", "baixar")

    def get_gazette_date(self, response_item):
        """
        Get the date for the gazette inside one of the 'box-diario' divs
        """
        date = response_item.css("span.data-diario::text").get().strip()
        return get_date_from_text(date)

    def get_edition_number(self, response_item):
        """
        Get the edition number inside one of the 'box-diario' divs
        """
        return response_item.css("h2::text").re_first(r"Edição\s+([.\d]+)")
