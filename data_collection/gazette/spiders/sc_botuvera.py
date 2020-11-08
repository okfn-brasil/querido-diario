from gazette.spiders.base import FecamGazetteSpider


class ScBotuveraSpider(FecamGazetteSpider):
    name = "sc_botuvera"
    FECAM_QUERY = "cod_entidade:48"
    TERRITORY_ID = "4202701"
