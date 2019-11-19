from gazette.spiders.base import FecamGazetteSpider


class ScGuaraciabaSpider(FecamGazetteSpider):
    name = "sc_guaraciaba"
    FECAM_QUERY = 'cod_entidade:105'
    TERRITORY_ID = "4206405"