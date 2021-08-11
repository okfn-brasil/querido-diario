from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuaracaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3517802"
    name = "sp_guaracai"
    allowed_domains = ["glicerio.sp.gov.br"]

    city = "guaracai"
