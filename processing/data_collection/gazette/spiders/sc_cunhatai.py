from gazette.spiders.base import FecamGazetteSpider


class ScCunhataiSpider(FecamGazetteSpider):
    name = "sc_cunhatai"
    FECAM_QUERY = "cod_entidade:81"
    TERRITORY_ID = "4204756"
