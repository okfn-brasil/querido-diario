from gazette.spiders.base import FecamGazetteSpider


class ScIpuacuSpider(FecamGazetteSpider):
    name = "sc_ipuacu"
    FECAM_QUERY = 'cod_entidade:122'
    TERRITORY_ID = "4207684"