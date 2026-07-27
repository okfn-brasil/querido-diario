from datetime import date

from gazette.spiders.base.ciga_sc import BaseCigaSCSpider


class ScFlorianopolisCigaSpider(BaseCigaSCSpider):
    """
    Spider para o Diário Oficial de Florianópolis/SC usando o sistema CIGA/SC.
    
    Este é um exemplo de como usar o spider base BaseCigaSCSpider para um
    município específico. O município_id 146 é o código de Florianópolis no
    sistema CIGA/SC.
    
    Para encontrar o município_id de outros municípios, você pode:
    1. Acessar https://edicao.dom.sc.gov.br/?r=site/edicoes
    2. Selecionar o município no filtro
    3. Ver o parâmetro Edicao[cod_municipio] na URL
    
    Exemplo de uso:
        scrapy crawl sc_florianopolis_ciga -a start=2024-08-01 -a end=2024-08-31
    """
    name = "sc_florianopolis_ciga"
    TERRITORY_ID = "4205407"  # Código IBGE de Florianópolis
    municipality_id = "146"  # Código de Florianópolis no sistema CIGA/SC
    start_date = date(2024, 8, 5)  # Data de início da publicação no sistema
    
