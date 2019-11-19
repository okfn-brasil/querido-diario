from gazette.spiders.base import FecamGazetteSpider


class ScGraoParaSpider(FecamGazetteSpider):
    name = "sc_grao_para"
    FECAM_QUERY = 'cod_entidade:102'
    TERRITORY_ID = "4206108"