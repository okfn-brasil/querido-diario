from gazette.spiders.base.fecam import FecamGazetteSpider


class ScVitorMeirelesSpider(FecamGazetteSpider):
    name = "sc_vitor_meireles"
    FECAM_QUERY = "cod_entidade:291"
    TERRITORY_ID = "4219358"
