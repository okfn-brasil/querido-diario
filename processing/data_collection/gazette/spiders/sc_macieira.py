from gazette.spiders.base import FecamGazetteSpider


class ScMacieiraSpider(FecamGazetteSpider):
    name = "sc_macieira"
    FECAM_QUERY = "cod_entidade:156"
    TERRITORY_ID = "4210050"
