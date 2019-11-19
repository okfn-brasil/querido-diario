from gazette.spiders.base import FecamGazetteSpider


class ScCamposNovosSpider(FecamGazetteSpider):
    name = "sc_campos_novos"
    FECAM_QUERY = 'cod_entidade:60'
    TERRITORY_ID = "4203600"