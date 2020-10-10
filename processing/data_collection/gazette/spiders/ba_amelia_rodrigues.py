from datetime import date, datetime
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
import scrapy


def get_next_month(current_date):
    # https://stackoverflow.com/a/22236549
    month = (current_date.month % 12) + 1
    year = current_date.year + (current_date.month + 1 > 12)
    return date(year, month, 1)


def extract_public_url(file_url):
    if not file_url:
        return
    # download: http://www.imprensaoficial.org/pub/prefeituras/ba/ameliarodrigues/2020/proprio/1582.pdf
    # original: http://www.imprensaoficial.org/pdf/baixar.php?
    # arquivo=../pub/prefeituras/ba/ameliarodrigues/2020/proprio/1582.pdf
    index = file_url.find("arquivo=../") + 11
    return f"http://www.imprensaoficial.org/{file_url[index:]}"


class BaAmeliaRodriguesSpider(BaseGazetteSpider):

    name = "ba_amelia_rodrigues"
    allowed_domains = ["pmameliarodriguesba.imprensaoficial.org"]
    start_date = date(2020, 9, 1)  # FIXME

    TERRITORY_ID = "2901106"

    def start_requests(self):
        """Gera as requests as páginas dos Diários."""
        current_date = self.start_date
        while current_date <= date.today():
            year_month = current_date.strftime("%Y/%m")  # like 2015/01
            # format http://pmameliarodriguesba.imprensaoficial.org/2015/01/
            url = f"http://pmameliarodriguesba.imprensaoficial.org/{year_month}/"
            current_date = get_next_month(current_date)
            yield scrapy.Request(url, callback=self.extract_gazette_links)

    def extract_gazette_links(self, response):
        # pagination exists when the button "Publicações mais antigas" is in the page
        another_page = response.xpath(
            ".//a[contains(text(), 'Publicações mais antigas')]/@href"
        ).extract_first()
        # or response.css("div.nav-previous a::attr(href)").extract_first()

        for a in response.css("h2 a"):
            yield scrapy.Request(a.attrib["href"], callback=self.parse)

        if another_page:
            yield scrapy.Request(another_page, callback=self.extract_gazette_links)

    def parse(self, response):
        file_url = response.css("div.entry-content a::attr(href)").extract_first()
        file_url = extract_public_url(file_url)

        gazette_date = response.css(
            "span.posted-on a time::attr(datetime)"
        ).extract_first()
        gazette_date = datetime.strptime(gazette_date, "%Y-%m-%dT%H:%M:%S%z").date()

        yield Gazette(
            date=gazette_date,
            file_urls=[file_url],
            is_extra_edition=False,  # TODO
            territory_id=self.TERRITORY_ID,
            power="executive",
            scraped_at=datetime.utcnow(),
        )
