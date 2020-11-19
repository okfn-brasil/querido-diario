from gazette.spiders.base import FecamGazetteSpider


class ScPraiaGrandeSpider(FecamGazetteSpider):
    name = "sc_praia_grande"
    FECAM_QUERY = "cod_entidade:209"
    TERRITORY_ID = "4213807"
