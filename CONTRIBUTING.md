# Contribuindo - Versão em Portugûes

*Observe que este projeto é lançado com um [Código de Conduta do Contribuidor](CODE_OF_CONDUCT.md). Ao participar deste projeto, você concorda em cumprir seus termos.*

Como o Diário Oficial busca se tornar uma fonte confiável de anúncios oficiais do governo, toda fonte de dados também deve ser confiável. Uma empresa privada que publica jornais do governo sem permissão oficial, por exemplo, não é uma fonte confiável.

Neste momento, o projeto visa os 100 principais municípios brasileiros por população, coletando todos os diários desde 2015. Se você quiser nos ajudar a atingir essa meta, estamos acompanhando o progresso dos rastreadores em [CITIES.md](CITIES. md) arquivo. Dê uma olhada se você quiser saber onde os colaboradores já estão trabalhando.

## Começando a contribuir

Se você nunca contribuiu em nenhum projeto de código aberto, existem tarefas apenas para você. Eles são [rotulados como "boa primeira edição"](https://github.com/okfn-brasil/diario-oficial/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22 ). Antes de começar, deixe um comentário dizendo que planeja trabalhar nisso e se tiver dúvidas significativas.

Às vezes, a comunidade organiza eventos para resolver vários problemas em um curto espaço de tempo. Especialmente nesses casos, um problema ou pull request pode ser considerado abandonado quando está aguardando o colaborador, mas não recebe atualizações por algumas semanas. Basta nos informar que você precisa de mais tempo, para que não acabemos fechando por engano.

### Configuração

Consulte o [arquivo README](README.md) para configurar o projeto. Além disso, leia o `Makefile` para entender as tarefas disponíveis e o que elas executam.

### Escrevendo crawlers para novos municípios

Para coletar os diários dos sites oficiais, usamos uma estrutura de rastreamento
chamado [Scrapy](https://docs.scrapy.org). Você pode encontrar seu
[tutorial oficial](https://docs.scrapy.org/en/latest/intro/tutorial.html) útil
para começar com a arquitetura. Nosso projeto pode ser encontrado no
pasta [`data_collection`](data_collection).

Dois comandos podem ser especialmente úteis: `scrapy shell` e `scrapy crawl`.

O Scrapy tem uma interface de shell para experimentar rastreadores ou aranhas (como
prefere chamá-lo). Para ver como o framework lê uma página da web antes de escrever um
spider para isso, tente o seguinte, onde você pode substituir o URL por um
site do município:

```consola
$ shell scrapy http://www2.portoalegre.rs.gov.br/dopa/
```

Para executar um spider existente, consulte o [arquivo README](README.md).

## Formatação de código automatizada

O projeto usa [Black](https://github.com/psf/black) como uma ferramenta automatizada para formatar e verificar o estilo do código e
[isor](https://github.com/pycqa/isor) para classificar as importações. O CI **falhará** se seu código não estiver correto
formatado de acordo com essas ferramentas.

Se você seguiu as instruções de configuração, instalando ganchos de pré-commit, é possível que você nunca
precisa executar essas ferramentas manualmente, pois elas serão executadas antes de cada commit. No entanto, se você quiser
para executá-los em todos os arquivos do projeto, você tem o comando `make format` que chamará essas ferramentas.

## Diretrizes para mantenedores

Esta seção é um espaço para mantenedores de projetos, pois como a revisão de código e a organização do repositório fazem parte do processo de contribuição, todas as diretrizes de revisão de código são de interesse público para qualquer pessoa da comunidade.

### Responsabilidades de um mantenedor do Querido Diario:

- Respeite o [código de conduta](https://github.com/okfn-brasil/querido-diario/blob/main/CODE_OF_CONDUCT.md) e garanta que quem possa ter sofrido assédio tenha um canal de ajuda.
- Sempre justifique uma sugestão de acordo com as práticas já adotadas no projeto, legibilidade e simplicidade. É fundamental que um projeto civil tenha uma estrutura o mais fácil possível para os iniciantes.
- Os mantenedores devem **executar todos os spiders antes de fundi-los**.
- Se um Pull Request tiver muitos commits e suas mensagens não estiverem claras, use a opção *Squash and merge*. Não é necessário fazer squash quando a disciplina de commits está boa, como exemplo: [Pull Request](https://github.com/okfn-brasil/querido-diario/pull/252/commits).


# Contributing - English Version

*Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.*

Since Diário Oficial seeks to become a trustful source of official governmental announcements, every data source must also be trustful. A private company publishing government gazettes without official permission, for instance, is not a trustful source.

At this moment, the project aims for the 100 top Brazilian municipalities by population, collecting all the gazettes since 2015. If you want to help us reach this goal, we're tracking the progress of crawlers in [CITIES.md](CITIES.md) file. Have a look at it if you want to know where contributors are already working.

## Starting to contribute

If you have never contributed to any open source project, there are tasks just for you. They are [labeled "good first issue"](https://github.com/okfn-brasil/diario-oficial/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Before starting, drop a comment saying you plan to work on it and if you have significant questions.

Sometimes the community organizes events for solving multiple issues in a short amount of time. Especially in these cases, an issue or pull request may be considered abandoned when is waiting for the contributor but doesn't receive updates for a couple of weeks. Just let us know you need more time, so we don't end up closing it by mistake.

### Setup

Please refer to the [README file](README.md) to set up the project. Also, read the `Makefile` for understanding the available tasks and what they run.

### Writing crawlers for new municipalities

For collecting the gazettes from the official websites, we use a crawling framework
called [Scrapy](https://docs.scrapy.org). You may find its
[official tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) helpful
to get started with the architecture. Our project can be found in the
[`data_collection`](data_collection) folder.

Two commands may especially be useful: `scrapy shell` and `scrapy crawl`.

Scrapy has a shell interface for experimenting with crawlers, or spiders (how
prefers to call it). To see how the framework reads a webpage before writing a
spider for it, try the following, where you can replace the URL for a different
municipality website:

```console
$ scrapy shell http://www2.portoalegre.rs.gov.br/dopa/
```

For running an existing spider, please refer to the [README file](README.md).

## Automated code formatting

Project uses [Black](https://github.com/psf/black) as an automated tool to format and check code style and
[isort](https://github.com/pycqa/isort) to sort the imports. CI will **fail** if your code are not correctly
formatted according these tools.

If you followed the setup instructions, installing pre-commit hooks, it is possible that you will never
need to run these tools manually, as they will be execute before each commit. However, if you want
to run them in all files in the project, you have `make format` command that will call these tools.

## Guidelines to maintainers

This section is a space for project maintainers, since as code review and repository organization are part of the contribution process, all code review guidelines are of public interest to anyone in the community.

### Responsibilities of a Querido Diario maintainer:

- Respect the [code of conduct](https://github.com/okfn-brasil/querido-diario/blob/main/CODE_OF_CONDUCT.md) and ensure that anyone who may have suffered harassment has a help channel.
- Always justify a suggestion according to the practices already adopted in the project, legibility and simplicity. It is essential for a civil project to have a structure as easy as possible for beginners.
- The maintainers should **run all the spiders before merging it**.
- If a Pull Request have many commits and their messages are not clear, use the *Squash and merge* option. It is not necessary to do squash when the commits discipline is good, as an example: [Pull Request](https://github.com/okfn-brasil/querido-diario/pull/252/commits).
