# Tutorial de debugging

Este tutorial reúne passos práticos para investigar problemas durante o desenvolvimento de raspadores do Querido Diário.

## Antes de começar

Ative o ambiente virtual e instale as dependências de desenvolvimento do projeto:

```console
source .venv/bin/activate
pip install -r data_collection/requirements-dev.txt
```

Execute os comandos a partir da pasta `data_collection`, onde está o projeto Scrapy:

```console
cd data_collection
```

## Reproduza o problema em um spider isolado

Comece executando somente o spider que apresenta falha. Isso reduz ruído no log e facilita repetir o teste após cada ajuste:

```console
scrapy crawl uf_municipio
```

Quando precisar limitar a quantidade de páginas processadas, use as configurações do Scrapy na própria chamada:

```console
scrapy crawl uf_municipio -s CLOSESPIDER_PAGECOUNT=1
```

Para salvar o resultado em um arquivo temporário e inspecionar os itens coletados:

```console
scrapy crawl uf_municipio -O /tmp/uf_municipio.json
```

## Aumente o detalhe dos logs

Use `LOG_LEVEL=DEBUG` quando precisar enxergar requisições, respostas, callbacks e mensagens internas do spider:

```console
scrapy crawl uf_municipio -s LOG_LEVEL=DEBUG
```

Se o log estiver muito grande, salve a saída para consultar depois:

```console
scrapy crawl uf_municipio -s LOG_LEVEL=DEBUG 2>&1 | tee /tmp/uf_municipio.log
```

Procure por mensagens como `ERROR`, `Traceback`, status HTTP inesperados, redirecionamentos e URLs repetidas.

## Inspecione seletores com o shell do Scrapy

Quando uma página não retorna os dados esperados, abra a URL no shell:

```console
scrapy shell "https://exemplo.gov.br/diario-oficial"
```

Dentro do shell, teste os seletores usados pelo spider:

```python
response.css("a::attr(href)").getall()
response.xpath("//a[contains(., 'Diário')]/@href").getall()
```

Essa etapa ajuda a separar problemas de seletor, paginação, codificação de texto e mudanças no HTML do site.

## Use breakpoints em callbacks

Para investigar o estado do spider durante a execução, adicione temporariamente um breakpoint no callback suspeito:

```python
def parse(self, response):
    breakpoint()
```

Depois execute o spider normalmente. No terminal interativo, consulte variáveis como `response.url`, `response.status`, `response.text`, `item` e listas intermediárias.

Remova o breakpoint antes de enviar a contribuição.

## Valide o resultado coletado

Depois de ajustar o spider, gere uma amostra e valide os campos principais:

```console
scrapy crawl uf_municipio -O /tmp/uf_municipio.json
python -m json.tool /tmp/uf_municipio.json | head
```

Confira se os itens possuem data, URL do diário, território correto e arquivos acessíveis. Quando a falha envolver mudança de site, inclua no pull request um resumo curto do que mudou e como a correção foi verificada.
