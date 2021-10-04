from gazette.spiders.base.doem import DoemGazetteSpider


class SPSaoCarlosSpider(DoemGazetteSpider):
    TERRITORY_ID = "3548906"
    state_city_url_part = "sp/sao carlos"
    allowed_domains = ["saocarlos.sp.gov.br"]
    start_urls = ["http://www.saocarlos.sp.gov.br/index.php/diario-oficial.html"]
    start_date = datetime.date(2009, 6, 11)
