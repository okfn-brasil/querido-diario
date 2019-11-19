from gazette.spiders.base import FecamGazetteSpider


class ScArabutaSpider(FecamGazetteSpider):
    name = "sc_arabuta"
    FECAM_QUERY = 'cod_entidade:20'
    TERRITORY_ID = "4201273"