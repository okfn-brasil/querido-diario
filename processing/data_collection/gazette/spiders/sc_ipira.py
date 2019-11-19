from gazette.spiders.base import FecamGazetteSpider


class ScIpiraSpider(FecamGazetteSpider):
    name = "sc_ipira"
    FECAM_QUERY = 'cod_entidade:120'
    TERRITORY_ID = "4207601"