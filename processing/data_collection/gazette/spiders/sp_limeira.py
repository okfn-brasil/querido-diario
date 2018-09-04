import scrapy

from gazette.items import Gazette
from dateparser import parse
from gazette.spiders.base import BaseGazetteSpider


class SpLimeiraSpider(BaseGazetteSpider):
    TERRITORY_ID = "3526902"
    name = "sp_limeira"
    allowed_domains = ["limeira.sp.gov.br"]
    start_urls = [
        "http://serv42.limeira.sp.gov.br/jof/NetJornal_cns_edicoes_cons_site/index.php"
    ]

    def parse(self, response):
        # TODO: implement parse method
        print("TODO: implement parse method")
