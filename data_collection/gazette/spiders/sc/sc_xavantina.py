from gazette.spiders.base.fecam import FecamGazetteSpider


class ScXavantinaSpider(FecamGazetteSpider):
    name = "sc_xavantina"
    FECAM_QUERY = "cod_entidade:294"
    TERRITORY_ID = "4219606"
