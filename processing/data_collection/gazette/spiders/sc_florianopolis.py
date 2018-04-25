from datetime import date, datetime

from dateparser import parse
from dateutil.relativedelta import relativedelta
from scrapy import FormRequest, Spider

from gazette.items import Gazette


class ScFlorianopolisSpider(Spider):
    name = 'sc_florianopolis'
    URL = 'http://www.pmf.sc.gov.br/governo/index.php?pagina=govdiariooficial'
    MUNICIPALITY_ID = '4205407'
    AVAILABLE_FROM = date(2009, 6, 1)

    def start_requests(self):
        """The City Hall website publish the gazettes in a page with a form
        that allow users to browse through different years and months. This
        form sends requests via POST, so this method emulates a series of these
        POSTs."""
        target = date.today()
        while target >= self.AVAILABLE_FROM:
            year, month = str(target.year), str(target.month)
            data = dict(ano=year, mes=month, passo='1', enviar='')
            yield FormRequest(url=self.URL, formdata=data, callback=self.parse)
            target = target + relativedelta(months=1)

    def parse(self, response):
        """Parse each page. Eahc list all gazettes for a given month."""
        for link in response.css('ul.listagem li a'):
            url = self.get_pdf_url(response, link)
            if not url:
                continue

            yield Gazette(
                date=self.get_date(link),
                file_urls=(url,),
                is_extra_edition=None,
                municipality_id=self.MUNICIPALITY_ID,
                power='all',
                scraped_at=datetime.utcnow(),
            )

    @staticmethod
    def get_pdf_url(response, link):
        relative_url = link.css('::attr(href)').extract_first()
        if not relative_url.lower().endswith('.pdf'):
            return None

        return response.urljoin(relative_url)

    def get_date(self, link):
        *_, date_as_str = link.css('::text').extract()
        return parse(date_as_str.strip(), languages=('pt',)).date()
