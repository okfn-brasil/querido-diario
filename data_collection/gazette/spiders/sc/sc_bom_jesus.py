from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBomJesusSpider(FecamGazetteSpider):
    name = "sc_bom_jesus"
    FECAM_QUERY = "cod_entidade:44"
    TERRITORY_ID = "4202537"
