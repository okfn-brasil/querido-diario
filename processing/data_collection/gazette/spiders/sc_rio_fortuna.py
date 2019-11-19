from gazette.spiders.base import FecamGazetteSpider


class ScRioFortunaSpider(FecamGazetteSpider):
    name = "sc_rio_fortuna"
    FECAM_QUERY = 'cod_entidade:221'
    TERRITORY_ID = "4214904"