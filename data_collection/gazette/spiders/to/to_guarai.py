import datetime as dt
import re
import locale

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

FILE_NAME_PATTERN = r"Edição Ordinária ([\d\.]+) de (\d{2} de \w+ de \d{4})"
FILE_NAME_PATTERN_OLD = r"Edição\s+(\d+)\s+Ordinária\s+(\d{2} de \w+ de \d{4})"
DOM_URL_PATTERN = r"^https://guarai\.to\.gov\.br/portal/\d+/"


# Set locale to PT-BR to match month
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


class ToGuaraiSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = False

    name = "to_guarai"
    TERRITORY_ID = "1709302"
    allowed_domains = [
        "guarai.to.gov.br",
    ]
    start_date = dt.date(2017, 1, 1)

    def start_requests(self):
        # Start from main page and navigate
        yield scrapy.Request(
            f"https://guarai.to.gov.br/portal/category/diario-oficial/",
            callback=self.parse_pages,
        )

    def parse_pages(self, response):
        # init at first page
        max_page = -1

        # Get available pages from response
        page_links = response.xpath('//nav[@class="cb__pagination"]//a/@href').getall()
        for page_link in page_links:
            match = re.search(r"/page/(\d+)/", page_link)
            if match:
                max_page = max(max_page, int(match.group(1)))

        # Create page links from 1 to max_page
        pages = list(range(1, max_page + 1))
        for page in pages:
            yield scrapy.Request(
                f"https://guarai.to.gov.br/portal/category/diario-oficial/page/{page}",
            )

    def parse(self, response):
        # Get the all the unique links to all the specific pages
        # The page duplicates the URLs because of an icon
        hrefs = set(response.xpath("//body//a/@href").getall())

        # Filter to find the PDF pages URLs:
        filtered_hrefs = [href for href in hrefs if re.match(DOM_URL_PATTERN, href)]

        # Navigate to each page to download the file
        for href in filtered_hrefs:
            print(f"Sending request to {href}")
            # Fetch the document URL
            yield scrapy.Request(
                href,
                callback=self.parse_gazette_download_url,
            )

    def parse_gazette_download_url(self, response):
        # Get all the unique pdf urls
        pdf_selectors = response.css('a[href$=".pdf"]')

        # ignore the pdfemb-viewer
        filtered_selectors = [
            selector
            for selector in pdf_selectors
            if "pdfemb-viewer" not in selector.get()
        ]

        for pdf_selector in filtered_selectors:
            # Get the URL and the url text
            file_title = pdf_selector.xpath("text()").get().replace("\xa0", " ")
            file_url = pdf_selector.xpath("@href").get()

            # Ensure the URL is valid:
            if "https:" not in file_url:
                # It is common on old file structure to have missing protocol
                # eg: //guarai.to.gov.br/portal/storage/2018/06/DOM-489.pdf
                file_url = f"https:{file_url}"

            # Get the edition number and the date
            match = re.search(FILE_NAME_PATTERN, file_title)
            if not match:
                # Try to match with the old file naming structure
                match = re.search(FILE_NAME_PATTERN_OLD, file_title)

            if match:
                edition_number_str = match.group(1)
                date_str = match.group(2)

                # Convert edition number to integer
                edition_number = int(edition_number_str.replace(".", ""))

                # Convert date string to date object
                date_obj = dt.datetime.strptime(date_str, "%d de %B de %Y").date()

                gazette_item = Gazette(
                    date=date_obj,
                    edition_number=edition_number,
                    is_extra_edition=False,
                    power="legislative",
                    file_urls=[file_url],
                )

                yield gazette_item
