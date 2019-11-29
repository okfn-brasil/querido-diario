from gazette.spiders.base import FecamGazetteSpider


class ScNovaVenezaSpider(FecamGazetteSpider):
    name = "sc_nova_veneza"
    FECAM_QUERY = "cod_entidade:177"
    TERRITORY_ID = "4211603"
