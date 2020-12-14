from gazette.spiders.base.fecam import FecamGazetteSpider


class ScRioDoCampoSpider(FecamGazetteSpider):
    name = "sc_rio_do_campo"
    FECAM_QUERY = "cod_entidade:217"
    TERRITORY_ID = "4214508"
