from datetime import date, datetime

import scrapy

from gazette.items import Gazette


class ImprensaOficialSpider(BaseGazetteSpider):
    @staticmethod
    def _get_next_month(current_date):
        month = (current_date.month % 12) + 1
        year = current_date.year + (current_date.month + 1 > 12)
        return date(year, month, 1)

    @staticmethod
    def _extract_public_url(file_url):
        if not file_url:
            return
        # original: http://www.imprensaoficial.org/pdf/baixar.php?
        #           arquivo=../pub/prefeituras/ba/ameliarodrigues/2020/proprio/1582.pdf
        # download: http://www.imprensaoficial.org/pub/
        #           prefeituras/ba/ameliarodrigues/2020/proprio/1582.pdf
        index = file_url.find("arquivo=../") + 11
        return f"http://www.imprensaoficial.org/{file_url[index:]}"

    def start_requests(self):
        current_date = self.start_date
        while current_date <= date.today():
            year_month = current_date.strftime("%Y/%m")  # like 2015/01
            current_date = self._get_next_month(current_date)
            yield scrapy.Request(
                self.url_base.format(year_month), callback=self.extract_gazette_links
            )

    def extract_gazette_links(self, response):
        # pagination exists when the button "Publicações mais antigas" is in the page
        another_page = response.xpath(
            ".//a[contains(text(), 'Publicações mais antigas')]/@href"
        ).extract_first()

        for a in response.css("h2 a"):
            yield scrapy.Request(
                a.attrib["href"], callback=self.parse, dont_filter=True
            )

        if another_page:
            yield scrapy.Request(another_page, callback=self.extract_gazette_links)

    def parse(self, response):
        file_url = response.css("div.entry-content a::attr(href)").extract_first()
        file_url = self._extract_public_url(file_url)

        gazette_date = response.css(
            "span.posted-on a time::attr(datetime)"
        ).extract_first()
        gazette_date = datetime.strptime(gazette_date, "%Y-%m-%dT%H:%M:%S%z").date()

        yield Gazette(
            date=gazette_date,
            file_urls=[file_url],
            is_extra_edition=False,  # it wasn't possible to identify whenever is extra or not
            territory_id=self.TERRITORY_ID,
            power="executive",
            scraped_at=datetime.utcnow(),
        )
