from gazette.spiders.base.dosp import DospGazetteSpider
import datetime


class SpGuaracaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3517802"
    name = "sp_guaracai"
    allowed_domains = ["glicerio.sp.gov.br"]

    city = "guaracai"
    code = 4853
    start_date = datetime.date(2018, 9, 27)
