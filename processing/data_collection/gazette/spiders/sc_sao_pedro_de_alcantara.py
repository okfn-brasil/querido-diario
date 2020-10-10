from gazette.spiders.base import FecamGazetteSpider


class ScSaoPedroDeAlcantaraSpider(FecamGazetteSpider):
    name = "sc_sao_pedro_de_alcantara"
    FECAM_QUERY = "cod_entidade:259"
    TERRITORY_ID = "4217253"
