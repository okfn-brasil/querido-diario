from gazette.spiders.base.fecam import FecamGazetteSpider


class ScOuroSpider(FecamGazetteSpider):
    name = "sc_ouro"
    FECAM_QUERY = "cod_entidade:181"
    TERRITORY_ID = "4211801"
