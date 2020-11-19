from gazette.spiders.base import FecamGazetteSpider


class ScJacintoMachadoSpider(FecamGazetteSpider):
    name = "sc_jacinto_machado"
    FECAM_QUERY = "cod_entidade:136"
    TERRITORY_ID = "4208708"
