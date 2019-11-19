from gazette.spiders.base import FecamGazetteSpider


class ScPinheiroPretoSpider(FecamGazetteSpider):
    name = "sc_pinheiro_preto"
    FECAM_QUERY = 'cod_entidade:199'
    TERRITORY_ID = "4213005"