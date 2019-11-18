from gazette.spiders.base import FecamGazetteSpider


class ScTrezeTiliasSpider(FecamGazetteSpider):
    name = "sc_treze_tilias"
    FECAM_QUERY = 'cod_entidade:277'
    TERRITORY_ID = "4218509"