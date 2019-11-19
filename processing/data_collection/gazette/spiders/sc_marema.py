from gazette.spiders.base import FecamGazetteSpider


class ScMaremaSpider(FecamGazetteSpider):
    name = "sc_marema"
    FECAM_QUERY = 'cod_entidade:162'
    TERRITORY_ID = "4210555"