from gazette.spiders.base import FecamGazetteSpider


class ScIpumirimSpider(FecamGazetteSpider):
    name = "sc_ipumirim"
    FECAM_QUERY = 'cod_entidade:123'
    TERRITORY_ID = "4207700"