from gazette.spiders.base import FecamGazetteSpider


class ScTrevisoSpider(FecamGazetteSpider):
    name = "sc_treviso"
    FECAM_QUERY = 'cod_entidade:275'
    TERRITORY_ID = "4218350"