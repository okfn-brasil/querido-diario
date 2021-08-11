from gazette.spiders.base.fecam import FecamGazetteSpider


class ScHervalDoesteSpider(FecamGazetteSpider):
    name = "sc_herval_doeste"
    FECAM_QUERY = "cod_entidade:109"
    TERRITORY_ID = "4206702"
