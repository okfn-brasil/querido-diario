from gazette.spiders.base import FecamGazetteSpider


class ScBomJesusDoOesteSpider(FecamGazetteSpider):
    name = "sc_bom_jesus_do_oeste"
    FECAM_QUERY = 'cod_entidade:45'
    TERRITORY_ID = "4202578"