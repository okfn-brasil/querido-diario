from gazette.spiders.base import FecamGazetteSpider


class ScRioDoOesteSpider(FecamGazetteSpider):
    name = "sc_rio_do_oeste"
    FECAM_QUERY = 'cod_entidade:218'
    TERRITORY_ID = "4214607"