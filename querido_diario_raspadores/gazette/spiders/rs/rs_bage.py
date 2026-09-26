import datetime as dt

from gazette.spiders.base.serpro import BaseSerproSpider


class RsBageSpider(BaseSerproSpider):
    """
    Raspador de diários oficiais da Prefeitura Municipal de Bagé - RS.

    Município: Bagé - RS
    Código IBGE: 4301602
    Plataforma: SERPRO Gov.br Cidades (DOE - Documento Oficial Eletrônico)
    Iniciativa e desenvolvimento: Bagé Transparente (www.bagetransparente.com.br)
    """

    TERRITORY_ID = "4301602"
    name = "rs_bage"
    start_date = dt.date(2024, 11, 8)
    HASH_PREFEITURA = "eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="
