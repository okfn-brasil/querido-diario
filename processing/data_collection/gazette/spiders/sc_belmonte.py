from gazette.spiders.base import FecamGazetteSpider


class ScBelmonteSpider(FecamGazetteSpider):
    name = "sc_belmonte"
    FECAM_QUERY = 'cod_entidade:38'
    TERRITORY_ID = "4202156"