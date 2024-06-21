**Português (BR)** | [English (US)](/docs/README-en-US.md)

<p align="center">
  <a href="https://queridodiario.ok.org.br/sobre" target="_blank"> <img alt="Querido Diário" src="./images/querido-diario-logo.png" width="200">
  </a>
</p>

# Querido Diário
Dentro do [ecossistema do Querido Diário](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#ecossistema-do-querido-diario), este repositório é o responsável pela tarefa de **raspagem dos sites publicadores de diários oficiais**.

Conheça mais sobre as [tecnologias](https://queridodiario.ok.org.br/tecnologia) e a [história](https://queridodiario.ok.org.br/sobre) do projeto no [site do Querido Diário](https://queridodiario.ok.org.br)

# Sumário
- [Como contribuir](#como-contribuir)
- [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
- [Template para raspadores](#template-para-raspadores)
- [Como executar](#como-executar)
  - [Dicas de execução](#dicas-de-execução)
- [Solução de problemas](#solução-de-problemas)
- [Suporte](#suporte)
- [Agradecimentos](#agradecimentos)
- [Open Knowledge Brasil](#open-knowledge-brasil)
- [Licença](#licença)

# Como contribuir
<p>  
  <a href="https://www.catarse.me/queridodiario-okbr" target="_blank"> 
    <img alt="catarse" src="https://img.shields.io/badge/Catarse-Apoie%20o%20projeto-orange?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDMyNSA0NTUiIHdpZHRoPSIzMjUiIGhlaWdodD0iNDU1Ij4KCTx0aXRsZT5sb2dvLXYtY29yLXBvc2l0aXZvLWFpPC90aXRsZT4KCTxzdHlsZT4KCQkuczAgeyBmaWxsOiAjMTdhMzM4IH0gCgkJLnMxIHsgZmlsbDogIzdkYjkzZCB9IAoJCS5zMiB7IGZpbGw6ICNmMmJmMDAgfSAKCQkuczMgeyBmaWxsOiAjZjE5MTA2IH0gCgkJLnM0IHsgZmlsbDogI2VhNjYwYiB9IAoJCS5zNSB7IGZpbGw6ICNkZTMyODEgfSAKCTwvc3R5bGU+Cgk8ZyBpZD0iTGF5ZXIgMSI+CgkJPGcgaWQ9IiZsdDtHcm91cCZndDsiPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczAiIGQ9Im01Ni40IDI1Ni40cS0xLjggMy4xLTMuNCA2LjRjLTE1LjQgMzMuMS00LjcgNjMuMSAxNC44IDkyLjQgMTEuNiAxNy40IDguNiAzNi40LTEuOSA0Ny4zLTYgNi4zLTE0LjUgOS44LTIzLjIgOS43LTQuNSAwLTkuMS0wLjktMTMuNS0zLTYuMy0yLjktMTUuMS05LjEtMjIuMi0yOC43LTguOS0yNC4yLTkuMS01MS42IDIuNi03Ni44IDEwLjEtMjEuNiAyNi45LTM3LjggNDYuOC00Ny4zeiIvPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczEiIGQ9Im00Ni41IDMwNS44YzAuNSAyLjYgMSA1LjIgMS43IDcuOCAxMC41IDM4LjcgNDAuNyA1Ni41IDc3LjggNjcuNCAyMi4xIDYuNSAzMyAyNC43IDMxLjkgNDEuMi0wLjcgOS42LTUuMyAxOC41LTEyLjcgMjQuNi0zLjggMy4yLTguNCA1LjctMTMuNSA3LTcuNCAyLTE5LjIgMy0zOS4xLTguNC0yNC41LTE0LjItNDQuMS0zNy4yLTUyLTY2LjctNi44LTI1LjItNC4xLTUwLjggNS45LTcyLjl6Ii8+CgkJCTxwYXRoIGlkPSImbHQ7UGF0aCZndDsiIGNsYXNzPSJzMiIgZD0ibTczLjIgMzU0LjVjMi4yIDEuOCA0LjUgMy42IDYuOSA1LjMgMzYuMiAyNS4zIDc0LjMgMTguOSAxMTMuMiAxLjggMjMuMi0xMC4xIDQ1LjMtMi41IDU2IDEyLjIgNi4zIDguNiA4LjYgMTkuNCA2LjggMjkuNy0xIDUuNC0zLjEgMTAuNy02LjUgMTUuNS00LjggNi45LTE0IDE2LjEtMzguOSAyMC41LTMwLjcgNS40LTYzLjQtMC4xLTkwLjktMTkuNC0yMy42LTE2LjUtMzkuNC0zOS45LTQ2LjYtNjUuNnoiLz4KCQkJPHBhdGggaWQ9IiZsdDtQYXRoJmd0OyIgY2xhc3M9InMzIiBkPSJtMTMwLjEgMzc2LjZxNC43IDAuMSA5LjUtMC40YzQ4LjQtNC4zIDc2LTM2LjUgOTYuNy03OC41IDEyLjQtMjUgMzYuNC0zNC4xIDU1LjgtMjkuMyAxMS40IDIuOCAyMSAxMC4yIDI2LjcgMjAuMyAzIDUuMiA1IDExLjEgNS41IDE3LjYgMC45IDkuMi0wLjQgMjMuNC0xOC4zIDQ0LjctMjIgMjYuMy01My41IDQ0LjgtOTAuMyA0OC0zMS41IDIuOC02MS40LTUuOC04NS42LTIyLjR6Ii8+CgkJCTxwYXRoIGlkPSImbHQ7UGF0aCZndDsiIGNsYXNzPSJzNCIgZD0ibTE5My42IDM1NS4xYzIuNy0yLjIgNS4zLTQuNiA3LjgtNy4xIDM3LjctMzcuOCAzOC4xLTg0LjUgMjUuOS0xMzQuNS03LjItMjkuOCA2LjUtNTQuNSAyNi4zLTY0LjIgMTEuNS01LjYgMjQuOS02LjEgMzYuOC0xLjggNi4zIDIuMyAxMi4xIDUuOSAxNy4xIDExIDcuMiA3LjEgMTYuMiAyMC4xIDE2LjMgNTAuNiAwIDM3LjctMTMuNSA3NS42LTQyLjIgMTA0LjMtMjQuNiAyNC43LTU1LjkgMzguNi04OCA0MS43eiIvPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczUiIGQ9Im0yMzEuOSAyOTJjMC44LTQuNCAxLjQtOC45IDEuOC0xMy41IDYtNjkuMi0zMi42LTExNi04Ni41LTE1NS43LTMyLjItMjMuNi0zOS4xLTU5LjYtMjcuNS04NS44IDYuNy0xNS4zIDE5LjctMjcgMzUuMi0zMi42IDguMS0yLjkgMTctNC4yIDI2LjEtMy40IDEzLjIgMS4xIDMzIDYuNSA1OC42IDM2LjkgMzEuNSAzNy41IDQ5LjcgODYuNSA0NS4xIDEzOS4xLTMuOSA0NS4xLTIzLjQgODUuMS01Mi44IDExNXoiLz4KCQk8L2c+Cgk8L2c+Cjwvc3ZnPg==">
  </a>
</p> 

Agradecemos por considerar contribuir com o Querido Diário! :tada:

Você encontra como fazê-lo no [CONTRIBUTING.md](/docs/CONTRIBUTING.md)!

Além disso, consulte a [documentação do Querido Diário](https://docs.queridodiario.ok.org.br/pt-br/latest/) para te ajudar. 

# Ambiente de desenvolvimento
Você precisa ter [Python](https://docs.python.org/3/) (+3.0) e o framework [Scrapy](https://scrapy.org) instalados. 

Os comandos abaixo preparam o ambiente em sistema operacional Linux. Eles consistem em criar um [ambiente virtual de Python](https://docs.python.org/pt-br/3/library/venv.html), instalar os requisitos listados em `requirements-dev` e a ferramenta para padronização de código `pre-commit`.

``` console
python3 -m venv .venv
source .venv/bin/activate
pip install -r data_collection/requirements-dev.txt
pre-commit install
```

> A configuração em outros sistemas operacionais está disponível em ["como configurar o ambiente de desenvolvimento"](/docs/CONTRIBUTING.md#como-configurar-o-ambiente-de-desenvolvimento), incluindo mais detalhes para quem deseja contribuir com o desenvolvimento do repositório.

# Template para raspadores

Ao invés de começar um arquivo de raspador do zero, você pode inicializar um arquivo de código de raspador já no padrão do Querido Diário, a partir de um template. Para isso, faça: 

1. Vá para o diretório `data_collection`:
```console
cd data_collection
```
2. Acione o template:
```console
scrapy genspider -t qdtemplate <uf_nome_do_municipio> <https://sitedomunicipio...>
```

Um arquivo `uf_nome_do_municipio.py` será criado no diretório `spiders`, com alguns campos já preenchidos. O diretório é organizado por UF, lembre-se de mover o arquivo para o diretório adequado.

# Como executar
Para experimentar a execução de um raspador já integrado ao projeto ou testar o que esteja desenvolvendo, siga os comandos: 

1. Se ainda não o fez, ative o ambiente virtual no diretório `/querido-diario`:
``` console
source .venv/bin/activate
```
2. Vá para o diretório `data_collection`:
```console
cd data_collection
```
3. Verifique a lista de raspadores disponíveis:
```console
scrapy list
```
4. Execute um raspador da lista:
```console
scrapy crawl <nome_do_raspador>       //exemplo: scrapy crawl ba_acajutiba
```
5. Os diários coletados na raspagem serão salvos no diretório `data_collection/data`

## Dicas de execução
Além dos comandos acima, o Scrapy oferece outros recursos para configurar o comando de raspagem. Os recursos a seguir podem ser usados sozinhos ou combinados.  

* **Limite de data**  
Ao executar o item 4, o raspador coletará todos os diários oficiais do site publicador daquele município. Para execuções menores, utilize a flag de atributo `-a` seguida de:

`start_date=AAAA-MM-DD`: definirá a data inicial de coleta de diários.
```console
scrapy crawl <nome_do_raspador> -a start_date=<AAAA-MM-DD>
```
`end_date=AAAA-MM-DD`: definirá a data final de coleta de diários. Caso omitido, assumirá a data do dia em que está sendo executado.
```console
scrapy crawl <nome_do_raspador> -a end_date=<AAAA-MM-DD>
```

* **Arquivo de log**   
É possível enviar o log da raspagem para um arquivo ao invés de deixá-lo no terminal. Isto é particularmente útil quando se desenvolve um raspador que apresenta problemas e você quer enviar o arquivo de log no seu PR para obter ajuda. Para isso, use a flag de configuração `-s` seguida de:

`LOG_FILE=log_<nome_do_municipio>.txt`: definirá o arquivo para armazenar as mensagens de log.
```console
scrapy crawl <nome_do_raspador> -s LOG_FILE=log_<nome_do_municipio>.txt
```

* **Tabela de raspagem**   
Também é possível construir uma tabela que lista todos os diários e metadados coletados pela raspagem, ficando mais fácil de ver como o raspador está se comportando. Para isso, use a flag de saída `-o` seguida de um nome para o arquivo.
```console
scrapy crawl <nome_do_raspador> -o <nome_do_municipio>.csv
```

# Solução de problemas
Confira o arquivo de [solução de problemas](/docs/TROUBLESHOOTING.md) para resolver os problemas mais frequentes com a configuração do ambiente do projeto. 

# Suporte 
<p>  
  <a href="https://go.ok.org.br/discord" target="_blank">
    <img alt="Discord Invite" src="https://img.shields.io/badge/Discord-Entre%20no%20servidor-blue?style=for-the-badge&logo=discord" >
  </a>
</p>

Ingresse em nosso [canal de comunidade](https://go.ok.org.br/discord) para trocas sobre os projetos, dúvidas, pedidos de ajuda com contribuição e conversar sobre inovação cívica em geral.

# Agradecimentos
Este projeto é mantido pela Open Knowledge Brasil e possível graças às comunidades técnicas, às [Embaixadoras de Inovação Cívica](https://embaixadoras.ok.org.br/), às pessoas voluntárias e doadoras financeiras, além de universidades parceiras, empresas apoiadoras e financiadoras.

Conheça [quem apoia o Querido Diário](https://queridodiario.ok.org.br/apoie#quem-apoia).

# Open Knowledge Brasil
<p>
  <a href="https://twitter.com/okfnbr" target="_blank">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-_-blue?style=for-the-badge&logo=twitter">
  </a>
  <a href="https://www.instagram.com/openknowledgebrasil/" target="_blank">
    <img alt="Instagram Follow" src="https://img.shields.io/badge/Instagram-_-red?style=for-the-badge&logo=instagram">
  </a>
  <a href="https://www.linkedin.com/company/open-knowledge-brasil" target="_blank">
    <img alt="LinkedIn Follow" src="https://img.shields.io/badge/LinkedIn-_-9cf?style=for-the-badge&logo=linkedin">
  </a>
</p>

A [Open Knowledge Brasil](https://ok.org.br/) é uma organização da sociedade civil sem fins lucrativos, cuja missão é utilizar e desenvolver ferramentas cívicas, projetos, análises de políticas públicas, jornalismo de dados para promover o conhecimento livre nos diversos campos da sociedade. 

Todo o trabalho produzido pela OKBR está disponível livremente.

# Licença

Código licenciado sob a [Licença MIT](LICENSE.md).
