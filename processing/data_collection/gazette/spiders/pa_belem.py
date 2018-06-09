import scrapy
import json
import dateparser
from datetime import datetime
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BelemSpider(BaseGazetteSpider):
    TERRITORY_ID = '1501402'
    name = 'pa_belem'
    allowed_domains = ['www.belem.pa.gov.br']

    @staticmethod
    def form_body(first=0, rows=500):

        return (('javax.faces.partial.ajax', 'true'), ('javax.faces.source',
                'grdDiario'), ('javax.faces.partial.execute', 'grdDiario'),
                ('javax.faces.partial.render', 'grdDiario'), ('grdDiario',
                'grdDiario'), ('grdDiario_pagination', 'true'),
                ('grdDiario_first', str(first)), ('grdDiario_rows', str(rows)),
                ('grdDiario_encodeFeature', 'true'), ('frmGridDiario',
                'frmGridDiario7'))

    def form_request(self, meta):
        return scrapy.FormRequest(
            'http://www.belem.pa.gov.br/diarioom/index.jsf', self.parse,
            method="POST", formdata=self.form_body(
                first=meta['first'], rows=meta['rows']), meta=meta)

    def start_requests(self):
        meta = {'first': 0, 'rows': 500}
        yield self.form_request(meta)

    def parse(self, response):
        total_gazettes = json.loads(response.xpath(
            '//extension[@ln="primefaces"]/text()').extract_first()).get(
                'totalRecords')
        if total_gazettes < response.meta['first'] + response.meta['rows']:
            if response.meta['first'] == total_gazettes:
                raise StopIteration
            else:
                return self.form_request(
                    {'first': response.meta['first'], 'rows': (total_gazettes -
                     response.meta['first'])})
        gazettes = response.xpath("//update[@id='grdDiario']/text()"
                                  ).extract_first()
        gazettes = scrapy.selector.Selector(text=gazettes).xpath('//tr')
        for gazette in gazettes:
            date = gazette.xpath('./td[2]').extract_first()
            date = dateparser.parse(date, settings={'DATE_ORDER': 'DMY'})
            url = gazette.xpath('.//a/@href').extract_first()
            url = response.urljoin(url)
            is_extra_edition = False
            yield Gazette(date=date,
                          file_urls=[url],
                          is_extra_edition=is_extra_edition,
                          territory_id=self.TERRITORY_ID,
                          power='executive',
                          scraped_at=datetime.utcnow(),)
        yield self.form_request(
                {'first': response.meta['first'] + response.meta['rows'],
                 'rows':  response.meta['rows']})
