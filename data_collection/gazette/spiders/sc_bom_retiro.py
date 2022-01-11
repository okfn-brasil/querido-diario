from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBomRetiroSpider(FecamGazetteSpider):
    name = "sc_bom_retiro"
    FECAM_QUERY = "cod_entidade:46"
    TERRITORY_ID = "4202602"
