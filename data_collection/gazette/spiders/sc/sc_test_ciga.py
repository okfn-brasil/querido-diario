from datetime import date

from gazette.spiders.base.ciga_sc import BaseCigaSCSpider


class ScTestCigaSpider(BaseCigaSCSpider):
    """
    Spider de teste para o sistema CIGA/SC - Edição Geral.
    
    Este spider busca a "Edição Geral" que contém publicações de todos os
    municípios de Santa Catarina e AUTOMATICAMENTE fatia o PDF por município,
    gerando um arquivo individual para cada um.
    
    Fluxo:
    1. Baixa a Edição Geral (1 PDF grande)
    2. Extrai sumário (lista de municípios)
    3. Fatia o PDF em N arquivos (1 por município)
    4. Mapeia cada município para código IBGE
    5. Gera N items Gazette (1 por município)
    
    Exemplo de uso:
        scrapy crawl sc_test_ciga -a start=2026-01-14 -a end=2026-01-14
        
    Resultado esperado:
        - 1 requisição HTTP (download do PDF completo)
        - ~124 items gerados (1 por município que publicou)
        - PDFs salvos em /tmp/ciga_sc_split/YYYY-MM-DD_EDICAO/
    """
    name = "sc_test_ciga"
    TERRITORY_ID = "4200000"  # Código do estado de Santa Catarina
    municipality_id = "-1"  # -1 para Edição Geral (todos os municípios)
    start_date = date(2026, 1, 14)

    
