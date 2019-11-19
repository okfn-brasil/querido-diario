from gazette.spiders.base import FecamGazetteSpider


class ScRioDoSulSpider(FecamGazetteSpider):
    name = "sc_rio_do_sul"
    FECAM_QUERY = 'cod_entidade:219'
    TERRITORY_ID = "4214805"