from gazette.spiders.base import FecamGazetteSpider


class ScPomerodeSpider(FecamGazetteSpider):
    name = "sc_pomerode"
    FECAM_QUERY = 'cod_entidade:202'
    TERRITORY_ID = "4213203"