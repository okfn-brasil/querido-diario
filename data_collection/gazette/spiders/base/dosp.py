import re
import logging
import dateparser

from scrapy_selenium import SeleniumRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DospGazetteSpider(BaseGazetteSpider):
    allowed_domains = ["dosp.com.br", "imprensaoficialmunicipal.com.br"]

    # Must be defined into child classes
    city = None

    def start_requests(self):
        yield SeleniumRequest(
            url=f"https://imprensaoficialmunicipal.com.br/{self.city}", 
            callback=self.parse,
        )

    def go_to_next_page(self, driver):
        # I use find_elements to avoid errors
        next_btn = driver.find_elements_by_css_selector("#Pagination a.next")
        if next_btn:
            next_btn[0].click()
            return True
        return False


    def parse(self, response):
        DATE = 0
        # YEAR = 1 # In roman form
        EDITION = 2

        driver = response.request.meta['driver']

        while True:
            for a in driver.find_elements_by_css_selector("#jornal .lista a"):
                ps = a.find_elements_by_tag_name("p")

                if len(ps) != 3:
                    self.log("Strange clickable link: " + a.text, logging.WARNING)
                    continue
                
                date = re.search(r"\d{2}/\d{2}/\d{4}", ps[DATE].text)
                if not date:
                    self.log("Strange date: " + a.text, logging.WARNING)
                    continue

                edition_number = re.search(r"Edi..o: (\d+)", ps[EDITION].text)
                if not edition_number:
                    self.log("Strange edition number: " + a.text, logging.WARNING)
                    continue
                
                date = dateparser.parse(date.group(), languages=("pt",)).date()
                file_url = a.get_attribute("href")
                edition_number = edition_number.group()
                
                yield Gazette(
                    date=date,
                    file_urls=[file_url],
                    edition_number=edition_number,
                    power="executive_legislative",
                )
            
            if not self.go_to_next_page(driver):
                break
