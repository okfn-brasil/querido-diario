from gazette.spiders.base import FecamGazetteSpider


class ScGuatambuSpider(FecamGazetteSpider):
    name = "sc_guatambu"
    FECAM_QUERY = 'cod_entidade:108'
    TERRITORY_ID = "4206652"