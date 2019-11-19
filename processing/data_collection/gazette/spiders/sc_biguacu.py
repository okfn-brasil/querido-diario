from gazette.spiders.base import FecamGazetteSpider


class ScBiguacuSpider(FecamGazetteSpider):
    name = "sc_biguacu"
    FECAM_QUERY = 'cod_entidade:40'
    TERRITORY_ID = "4202305"