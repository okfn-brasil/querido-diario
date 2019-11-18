from gazette.spiders.base import FecamGazetteSpider


class ScVargemBonitaSpider(FecamGazetteSpider):
    name = "sc_vargem_bonita"
    FECAM_QUERY = 'cod_entidade:288'
    TERRITORY_ID = "4219176"