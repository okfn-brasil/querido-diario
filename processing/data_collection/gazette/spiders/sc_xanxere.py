from gazette.spiders.base import FecamGazetteSpider


class ScXanxereSpider(FecamGazetteSpider):
    name = "sc_xanxere"
    FECAM_QUERY = 'cod_entidade:293'
    TERRITORY_ID = "4219507"