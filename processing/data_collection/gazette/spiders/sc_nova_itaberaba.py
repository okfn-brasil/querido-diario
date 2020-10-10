from gazette.spiders.base import FecamGazetteSpider


class ScNovaItaberabaSpider(FecamGazetteSpider):
    name = "sc_nova_itaberaba"
    FECAM_QUERY = "cod_entidade:175"
    TERRITORY_ID = "4211454"
