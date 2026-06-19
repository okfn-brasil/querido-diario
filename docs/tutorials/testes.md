# Tutorial de testes

Este tutorial mostra os principais testes usados durante contribuições no Querido Diário. Ele serve como um roteiro rápido para validar mudanças em raspadores e em código de apoio antes de abrir uma pull request.

## Pré-requisitos

Siga primeiro a configuração descrita no [guia de contribuição](../CONTRIBUTING.md#como-configurar-o-ambiente-de-desenvolvimento). Com o ambiente virtual ativo, instale as dependências de desenvolvimento:

```console
pip install -r data_collection/requirements-dev.txt
```

Execute os comandos abaixo a partir da raiz do repositório, salvo quando indicado o contrário.

## Testes automatizados

A suíte automatizada fica em `data_collection/tests` e pode ser executada com `pytest`:

```console
pytest data_collection/tests
```

Durante o desenvolvimento, rode apenas o recorte relacionado à alteração para receber retorno mais rápido. Alguns exemplos úteis:

```console
pytest data_collection/tests/test_dates.py
pytest data_collection/tests/test_extraction.py
pytest data_collection/tests -k nome_do_teste
```

Quando a alteração afetar parsing de datas, extração de metadados, pipelines ou utilitários compartilhados, rode também a suíte completa antes de enviar a pull request.

## Teste manual de raspador

Para testar um raspador, entre no diretório `data_collection`:

```console
cd data_collection
```

Liste os raspadores disponíveis:

```console
scrapy list
```

Execute uma coleta pequena usando uma data inicial e final. Esse formato ajuda a reproduzir o teste e evita baixar todo o histórico do município durante a validação inicial:

```console
scrapy crawl <nome_do_raspador> -a start=AAAA-MM-DD -a end=AAAA-MM-DD -s LOG_FILE=log_<nome_do_raspador>.txt -o <nome_do_raspador>.csv
```

Confira o arquivo `.log` para erros, redirecionamentos inesperados e mensagens de retry. Depois, abra o `.csv` e valide se os campos essenciais estão preenchidos, especialmente data, edição, URL do arquivo e poder responsável quando aplicável.

## Coleta da última edição

Para confirmar que o raspador ainda encontra publicações recentes, execute uma coleta sem `start` e com `end` no dia atual ou em uma data próxima conhecida:

```console
scrapy crawl <nome_do_raspador> -a end=AAAA-MM-DD -s LOG_FILE=log_<nome_do_raspador>_ultima_edicao.txt -o <nome_do_raspador>_ultima_edicao.csv
```

Esse teste é útil para manutenção de raspadores em produção, porque detecta mudanças recentes no site publicador.

## Antes de abrir a pull request

Revise estes pontos:

- Os testes automatizados relevantes passaram.
- A coleta manual gerou `.log` sem erros inesperados.
- O `.csv` contém os metadados obrigatórios dos diários coletados.
- Alguns arquivos baixados foram abertos manualmente para conferir se são diários oficiais válidos.
- Os comandos executados e arquivos de evidência necessários estão prontos para serem descritos na pull request.

Se algum teste não puder ser executado, explique o motivo na descrição da pull request e informe qual validação alternativa foi feita.