"""
Spider
Thiago Nobrega
"""
import dateparser
from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbCampinaGrandeSpiderExecutive(BaseGazetteSpider):

    TERRITORY_ID = "2504009"
    allowed_domains = ["campinagrande.pb.gov.br"]
    name = "pb_campina_grande_executive"
    start_urls = ["http://campinagrande.pb.gov.br/semanario-oficial/"]

    def parse(self, response):
        """
        @url http://campinagrande.pb.gov.br/semanario-oficial/
        @scrapes date file_urls territory_id power scraped_at
        """
        for href in response.xpath("//div[@class='secretaria-text']/a/@href").extract():
            yield Request(href, self.find_gazettes_by_month)

    def find_gazettes_by_month(self,response):
        """
            Get gazetes by month of the year
        :param response: url to gazzetes of the year
        """
        for href in response.xpath("//div[@class='secretaria-text']/a/@href").extract():
            yield Request(href, self.get_gazettes)


    def get_gazettes(self,response):
        """
            List gazettes of month
        :param response: url
        """
        editions = response.xpath("//div[@class='td_module_1 td_module_wrap td-animation-stack td_module_no_thumb']")
        # fixing problems where the gazette url is in the month... For same unknow resont the mayor realese all gazetes in one edition (shouul be 4 editions by month)
        if len(editions) == 0:
            yield Request(response.url, self.get_pdfurl, meta={'author': None, 'posttime': None})
        else:
            for edition in editions:
                pdfurl = response.xpath("//h3[@class='entry-title td-module-title']/a/@href").extract_first()
                post_author = response.xpath("//span[@class='td-post-author-name']/a/text()").extract_first()
                post_time = response.xpath("//time[@class='entry-date updated td-module-date']/text()").extract_first()

                yield Request(pdfurl, self.get_pdfurl, meta={'author': post_author,'posttime':post_time})

    def get_pdfurl(self,response):
        """
            Return the gazette with url,date (gazette and scraped) and file_urls
        """
        post_author = response.meta.get('author')
        pt = response.meta.get('posttime')
        if pt == None:
            post_time = None
        else:
            post_time = dateparser.parse(pt).date()

        from scrapy.selector import Selector
        hxs = Selector(response)

        file_url = hxs.xpath("//div[@class='td-post-content']/p/a/@href").extract_first()
        #fixing problems where the gazette url is in the month... For same unknow resont the mayor realese all gazetes in one edition (shouul be 4 editions by month)
        if file_url == None:
            file_url = hxs.xpath("//p[@class='embed_download']/a/@href").extract_first()

        g = Gazette(
            date=post_time,
            file_urls=[file_url],
            territory_id=self.TERRITORY_ID,
            power="executive",
            scraped_at=datetime.utcnow(),
        )
        if file_url==None:
            print(response)
            print(g)
        return g