from gazette.spiders.base import FecamGazetteSpider


class ScGalvaoSpider(FecamGazetteSpider):
    name = "sc_galvao"
    FECAM_QUERY = 'cod_entidade:97'
    TERRITORY_ID = "4205605"