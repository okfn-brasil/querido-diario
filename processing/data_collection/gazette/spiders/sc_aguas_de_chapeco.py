from gazette.spiders.base import FecamGazetteSpider


class ScAguasDeChapecoSpider(FecamGazetteSpider):
    name = "sc_aguas_de_chapeco"
    FECAM_QUERY = 'cod_entidade:9'
    TERRITORY_ID = "4200507"