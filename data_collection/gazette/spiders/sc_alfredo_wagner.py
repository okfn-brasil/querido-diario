from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAlfredoWagnerSpider(FecamGazetteSpider):
    name = "sc_alfredo_wagner"
    FECAM_QUERY = "cod_entidade:12"
    TERRITORY_ID = "4200705"
