# Querido Diário

_Última atualização: 16/10/2021._
______________________________________

_[Click here](languages/en-US/README.md) to read this article in english._
______________________________________

**Diário Oficial** é o nome da publicação utilizada pela administração pública brasileira para comunicar suas ações à população. Para ser válido, todo ato público deve ser publicado no diário oficial, seja na esfera federal, estadual ou municipal. 

Mesmo com os esforços recorrentes para fortalecer a [Lei de Acesso à Informação](http://www.acessoainformacao.gov.br/assuntos/conheca-seu-direito/principais-aspectos/principais-aspectos) pelo país, a comunicação oficial permanece - na maioria do território nacional - em PDFs.

O objetivo do **Querido Diário** é trazer os _diários oficiais municipais_ para a era digital, centralizando as informações hoje disponíveis apenas em fontes separadas. 

O projeto tinha duas metas distintas quando foi lançado: criar raspadores para os diários oficiais e analisar as informações sobre compras públicas e licitações. Atualmente, mantemos apenas o primeiro deles. 

Para saber mais sobre o projeto, acesse o [site oficial](https://queridodiario.ok.org.br/). 

Tabela de Conteúdos
=================
  * [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
    * [Rodar o raspador](#rodar-o-raspador)
    * [Gerar múltiplos raspadores a partir de um template](#gerar-múltiplos-raspadores-a-partir-de-um-template)
  * [Solução de problemas](#solução-de-problemas)
  * [Contribuindo](#contribuindo)
  * [Créditos](#créditos)

## Ambiente de desenvolvimento

A melhor maneira de entender como o **Querido Diário** funciona é acessar a fonte original e rodá-la localmente. Todos os raspadores são desenvolvidos usando o framework [Scrapy](https://scrapy.org). Eles oferecem um [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) para que você aprenda como usá-lo.

Se você utiliza Windows, antes de rodar os passos a seguir, você irá precisar do Microsoft Visual Build Tools (baixe [aqui](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/)). Ao iniciar a instalação, você precisa selecionar 'C++ build tools' na aba de carregamento e também 'Windows 10 SDK' e 'MSVC v142 - VS 2019 C++ x64/x86 build tools' na aba de componentes individuais.

Se você utiliza Linux, os comandos a seguir irão criar um novo [ambiente virtual](https://docs.python.org/pt-br/3/library/venv.html) - que manterá tudo isolado do seu sistema -, ativá-lo e  instalar todas as bibliotecas necessárias para começar a rodar e desenvolver novos raspadores.

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r data_collection/requirements-dev.txt
$ pre-commit install
```

No sistema Windows, você pode utilizar o código abaixo. Apenas substitua ```source .venv/bin/activate ``` por ```.venv/Scripts/activate.bat```. Os outros passos são os mesmos usados no Linux. 


### Rodar o raspador 

Depois de configurar o ambiente de desenvolvimento, você poderá desenvolver e executar novos raspadores. Os raspadores estão na pasta `data_collection`, então você deve entrar nela e executar o comando `scrapy`:

```console
$ cd data_collection
```

A seguir, listamos alguns comandos úteis.

Obter a lista de raspadores disponíveis

```console
$ scrapy list
```
Executar o raspador com o nome `spider_name`:

> Atenção: o comando acima levará um tempo para ser finalizado e irá coletar o site inteiro por padrão. Se você deseja pará-lo antes disso ou limitar a execução, utilize [CLOSESPIDER_ITEMCOUNT](https://docs.scrapy.org/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_ITEMCOUNT) ou configure `start_date` no raspador para uma data mais próxima.

```console
$ scrapy crawl spider_name
```
Você pode limitar o número de diários que deseja baixar configurando `start_date` como um argumento com o formato `YYYY-MM-DD`. O comando a seguir irá baixar apenas diários cuja data é maior que 01/09/2020:

```console
$ scrapy crawl sc_florianopolis -a start_date=2020-09-01
```
Dados coletados serão salvos na pasta `data_collection/data`.

### Gerar múltiplos raspadores a partir de um template

Você pode se deparar com um cenário em que há diferentes cidades utilizando a mesma base para o raspador, como em `FecamGazetteSpider`. Para não ter que criar os arquivos de raspadores manualmente, você pode utilizar um script para casos em que temos alguns raspadores que não são complexos e usam a mesma base.

Os templates de raspadores ficam na pasta `scripts/`. Aqui está um exemplo de um raspador gerado: 

```
from datetime import date
from gazette.spiders.base import ImprensaOficialSpider


class BaGentioDoOuroSpider(ImprensaOficialSpider):

    name = "ba_gentio_do_ouro"
    allowed_domains = ["pmGENTIODOOUROBA.imprensaoficial.org"]
    start_date = date(2017, 2, 1)
    url_base = "http://pmGENTIODOOUROBA.imprensaoficial.org"
    TERRITORY_ID = "2911303"
```

Para rodar o script, você precisa apenas de um arquivo .CSV seguindo a estrutura a seguir: 

```
url,city,state,territory_id,start_day,start_month,start_year,base_class
http://pmXIQUEXIQUEBA.imprensaoficial.org,Xique-Xique,BA,2933604,1,1,2017,ImprensaOficialSpider
http://pmWENCESLAUGUIMARAESBA.imprensaoficial.org,Wenceslau Guimarães,BA,2933505,1,1,2017,ImprensaOficialSpider
http://pmVERACRUZBA.imprensaoficial.org,Vera Cruz,BA,2933208,1,4,2017,ImprensaOficialSpider
```

Depois de obter o arquivo .CSV, rode o comando: 

```
cd scripts/

python generate_spiders.py new-spiders.csv
```

É isso. O novo raspador estará na pasta `data_collection/gazette/spiders/`.

## Solução de problemas

### `Python.h` faltando

Ao rodar o comando `pip install`, você pode obter o seguinte erro:

```
module.c:1:10: fatal error: Python.h: No such file or directory
     #include <Python.h>
              ^~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```

Tente instalar `python3-dev`. Por exemplo, via `apt install python3-dev`, se você está usando uma distro Debian, ou utilize o gerenciamento de pacotes da sua distro (por exemplo, `python3.6-dev` or `python3.7-dev`). Você pode saber qual é a sua versão via `python3 --version`.

## Contribuindo
Se você está interessado em resolver issues e contribuir diretamente no código, por favor, leia o documento [CONTRIBUTING.md](CONTRIBUTING.md).

## Créditos

Este projeto é mantido pela [Open Knowledge Brasil](https://ok.org.br/) graças ao apoio da Digital Ocean e de [muitas outras pessoas](https://queridodiario.ok.org.br/apoie#quem-apoia).
