**Português (BR)** | [English (US)](/docs/CONTRIBUTING-en-US.md)

# Contribuindo
O Querido Diário possui um [Guia para Contribuição](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#contribuindo) principal que é relevante para todos os seus repositórios. Este guia traz informações gerais sobre como interagir com o projeto, o código de conduta que você adere ao contribuir, a lista de repositórios do ecossistema e as primeiras ações que você pode tomar. Recomendamos sua leitura antes de continuar.

Já leu? Então vamos às informações específicas deste repositório:
- [Estrutura](#estrutura)
- [Desafios](#desafios)
    - [Labels e Milestones](#labels-e-milestones)
    - [Prioridades](#prioridades)
- [Como escolher uma issue para fazer](#como-escolher-uma-issue-para-fazer)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
    - [Em Linux](#em-linux)
    - [Em Windows](#em-windows)
  - [Formatação automática de código](#formação-automática-de-código)
- [Mantendo](#mantendo)
    - [Revisão de raspadores](#revisão-de-raspadores)

## Estrutura

Uma breve descrição da estrutura do repositório:

| **Diretório** | **Descrição** |
| ------------- | ------------- |
| [`.github`](/.github) | Diretório com configurações do repositório para o GitHub |
| [`.github/workflows`](/.github/workflows) | Configurações das GitHub Actions do repositório (fluxos de raspagens, deploy em produção, etc) |
| [`docs`](/docs) | Diretório de arquivos de documentação do repositório (README, CONTRIBUTING, etc) |
| [`templates/spiders`](/querido_diario/templates/spiders) | Diretório para templates de spiders pré-configurados no formato padrão do repositório |
| [`querido_diario`](/querido_diario) | Diretório para projeto Scrapy de coleta de dados adaptado para as necessidades do Querido Diário |
| [`querido_diario/gazette/database`](/querido_diario/gazette/database) | Diretório para o modelo de banco de dados |
| [`querido_diario/gazette/resources`](/querido_diario/gazette/resources) | Diretório para recursos adicionais: tabela de códigos IBGE dos municípios e esquema para validação dos dados de coleta |
| [`querido_diario/gazette/spiders`](/querido_diario/gazette/spiders) | Diretório para as spiders dos municípios organizado por estado |
| [`querido_diario/gazette/spiders/base`](/querido_diario/gazette/spiders/base) | Diretório de spiders base para [padrões identificados em sites](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/lista-sistemas-replicaveis.html) |

## Desafios
O principal desafio aqui é o de ter cada vez mais raspadores de sites publicadores de diários oficiais, visando atingir os 5570 municípios brasileiros. Utilizamos o [Quadro de Expansão de Cidades](https://github.com/orgs/okfn-brasil/projects/12/views/13) para organizar as tarefas mais visualmente. Consulte-o para localizar tarefas relevantes com as quais você pode contribuir.

Para te ajudar a desenvolver, utilize as orientações da página ["raspadores"](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html) disponível na [documentação técnica do Querido Diário](https://docs.queridodiario.ok.org.br/).

### Labels e Milestones
As *issues* são marcadas com etiquetas (*labels*) e/ou agrupadas em metas (*milestones*), um recurso que serve para classificá-las quanto ao tipo, destacando diferentes aspectos de interesse que podem ter. Navegar na seção de [labels](https://github.com/okfn-brasil/querido-diario/labels) e [milestones](https://github.com/okfn-brasil/querido-diario/milestones) facilita para encontrar uma *issues* mais do perfil do que gostaria de fazer.

### Prioridades
Para garantir que nossos esforços estejam alinhados e focados em objetivos claros, definimos prioridades para o
repositório. Nós endereçamos as *issues* e a fila de revisões seguindo esses critérios. Sua contribuição pode ser ainda mais valiosa quando alinhada com as prioridades.

| Prioridade | Descrição | Onde encontrar |
| ---------- | --------- | -------------- |
| 1 | Manutenção de raspadores em produção | [`maintenance`](https://github.com/okfn-brasil/querido-diario/labels/maintenance) |
| 2 | Adição de raspadores para municípios solicitados por alguma organização parceira | podem ser marcadas com [`priority`](https://github.com/okfn-brasil/querido-diario/labels/priority) |
| 3 | Implementação de melhorias estruturais no repositório | [`enhancement`](https://github.com/okfn-brasil/querido-diario/labels/enhancement) |
| 4 | Adição de spider base | [`spider-base`](https://github.com/okfn-brasil/querido-diario/labels/spider-base) |
| 5 | Adição de raspador para município que é capital | [`capitais`](https://github.com/okfn-brasil/querido-diario/milestone/2) |
| 6 | Adição de raspador para município da Amazônia Legal | [`100 cidades da Amazônia Legal`](https://github.com/okfn-brasil/querido-diario/milestone/5) |
| 7 | Adição de raspador para município que é populoso | [`100 cidades populosas`](https://github.com/okfn-brasil/querido-diario/milestone/4) |
| 8 | Adição de raspador não associado às metas | sem *label* |


## Como escolher uma issue para fazer
O repositório tem tarefas bem delimitadas e, no geral, bem isoladas entre si. Isso é uma vantagem: permite à comunidade contribuidora ter boas opções de tarefas, com diferentes dificuldades, cobrindo de pessoas iniciantes às mais experientes.

Por isso, esta seção traz os tipos de raspadores do repositório, suas complexidades, quais etiquetas são usadas neles e quais seções da documentação serão mais necessárias para fazê-los.

**Mas antes...** A seguir, você terá a progressão da complexidade das tarefas do repositório, do básico ao avançado. Coisa que, em outras palavras, é quase como uma jornada guiada. Se você se propor a vivê-la, pode ter uma experiência interessante de crescimento técnico ;)

1. Para município replicado
- Não há complexidade, pois envolve apenas criar e preencher [arquivos simples seguindo um padrão](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#ufmunicipiospider-para-uma-basesistemaspider-generica)
    - Uma vez que não tem complexidade no código em si, a tarefa possibilita experienciar o básico (usar do git/GitHub, fazer a configuração do ambiente, rodar um raspador, conhecer o básico do *log*, etc), além do gostinho de ter uma contribuição feita sem muito estresse.
- Onde encontrar essas tarefas? Elas são listas de municípios marcados com "boa primeira tarefa" ([`good first issue`](https://github.com/okfn-brasil/querido-diario/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+-label%3Aon-hold))
    - É uma modalidade de contribuição tão simples que, para valer o tempo de desenvolvimento e revisão, solicitamos que sejam enviados de 5 a 10 municípios por *pull request*. Deixe um comentário na *issue* avisando quais daquela lista vai fazer.
- Seções úteis da documentação:
    - Para fazer um raspador: [As classes BaseSistemaSpider](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#as-classes-basesistemaspider)
    - Para executar um raspador: [Executando raspadores](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#executando-raspadores)
    - Para validar uma coleta: [Validando raspagens](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#validando-raspagens)

2. Para município individual
- No caso anterior, o "grosso" do código de raspagem já estava implementado e o novo raspador apenas complementa com alguns dados, por isso era tão simples. Porém, agora nesses casos, deve-se ser implementada toda a lógica de raspagem.
    - Será necessário exercitar conhecimentos como inspeção de páginas, uso de seletores e expressões regulares.
- A dificuldade varia muito dependendo de como é o site a ser raspado e as barreiras que precisam ser superadas pelo raspador.
    - A grosso modo, pode-se dizer que os casos menos complexos é quando todos os diários são exibidos de uma vez em uma mesma página ou há uma paginação simples. A partir disso, a complexidade vai aumentando conforme uma ou mais barreiras vão aparecendo.
- Onde encontrar essas tarefas? Elas são marcadas com [`spider`](https://github.com/okfn-brasil/querido-diario/labels/spider) e também com o nível estimado de dificuldade: [`dificuldade:baixa`](https://github.com/okfn-brasil/querido-diario/labels/dificuldade%3Abaixa), [`dificuldade:media`](https://github.com/okfn-brasil/querido-diario/labels/dificuldade%3Amedia) e [`dificuldade:alta`](https://github.com/okfn-brasil/querido-diario/labels/dificuldade%3Aalta)
- Seções úteis da documentação:
    - [As classes UFMunicipioSpider](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#as-classes-ufmunicipiospider): todas as partes que o raspador deve ter e um modelo para o código
    - [Desenvolvendo raspadores](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#desenvolvendo-raspadores): as diretrizes de desenvolvimento e como superar algumas barreiras comuns em sites
    - [Fluxo de execução do Scrapy](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#fluxo-de-execucao): a ordem que o Scrapy aciona módulos de código quando uma raspagem é executada

3. Para sistema replicável
- Se no caso 1 a tarefa era simples por usar um código já implementado, aqui o desafio é justamente criar esse código generalizado para o padrão do sistema que outros raspadores vão poder usar
    - Por isso, é considerada uma tarefa mais complexa: é um exercício de abstração, adiciona mais linhas de código e afeta múltiplos raspadores.
    - Mas também é a mais impactante: cada padrão integrado permite integrar [dezenas de municípios](https://github.com/okfn-brasil/querido-diario/issues?q=is%3Aissue+is%3Aopen+label%3Aepic), aumentando a cobertura do Querido Diário rapidamente.
- Assim como o caso 2, a dificuldade varia muito e pelos mesmos motivos: depende das barreiras a serem superadas no site.
- Onde encontrar essas tarefas? Elas são marcadas com [`spider-base`](https://github.com/okfn-brasil/querido-diario/labels/spider-base)
- Seções úteis da documentação:
    - À essa altura, uma pessoa já entrou em contato com toda a [documentação sobre raspadores](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html) que deverá ser usada aqui, também.

### Contribua com revisão

Ao já ter desenvolvido todos os tipos de raspadores acima, experimente seguir contribuindo com o repositório por meio de revisões.

## Como configurar o ambiente de desenvolvimento
Os raspadores são desenvolvidos usando [Python](https://docs.python.org/3/) e o framework [Scrapy](https://scrapy.org). Você pode conferir [como instalar Python](https://www.python.org/downloads/) em seu sistema operacional e conhecer mais sobre o Scrapy [neste tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html). Com Python em seu computador, siga o passo-a-passo da configuração do ambiente de desenvolvimento:

### Em Linux
1. Faça um fork deste repositório e, com o terminal aberto em um diretório de preferência no seu computador, clone-o e acesse o novo diretório criado com o nome do repositório.
``` console
git clone <repositorio_fork>
cd querido-diario
```
2. Crie um novo [ambiente virtual](https://docs.python.org/pt-br/3/library/venv.html) - que manterá as execuções do projeto isoladas de seu sistema.
``` console
python3 -m venv .venv
```
3. Ative o recém criado ambiente virtual
``` console
source .venv/bin/activate
```
4. Instale as [bibliotecas requeridas](querido-diario/pyproject.toml).
``` console
pip install querido-diario[dev]
```
5. Instale o pré-commit, uma ferramenta que, ao fazer o _commit_ do código, verifica se ele se adequa aos padrões do projeto.
``` console
pre-commit install
```
6. Seu ambiente de desenvolvimento está pronto! :tada:

_Atenção:_ Estas etapas precisam ser executadas apenas na primeira vez que interagir com o projeto durante a preparação do ambiente. Depois disso, basta ativar o ambiente virtual (passo 3) cada vez que for utilizar ou contribuir com o repositório.

### Em Windows

#### Pelo terminal do Windows
As instruções a seguir foram experimentadas em Windows 10 e 11. Lembre-se que caso deseje realizar uma integração com o repositório [querido-diario-data-processing](https://github.com/okfn-brasil/querido-diario-data-processing) é preferível que a sua configuração de ambiente seja feita [utilizando WSL](CONTRIBUTING.md#utilizando-wsl).

1. Instale o [Visual Studio Comunidade](https://visualstudio.microsoft.com/pt-br/downloads/) . Ao abrir o terminal do instalado do Visual Studio, antes de instalar, você precisa selecionar na aba de  **Componentes Individuais** "SDK do Windows 10" ou "11" (a depender do seu sistema) e "Ferramentas de build do MSVC v143 - VS 2022 C++ x64/x86 (v14.32-17.4)". Note que muitas vezes as versões Windows 10 SDK e MSVC v142 - VS 2019 C++ x64/x86 build tools serão atualizadas, portanto procure por itens similares em Componentes individuais para realizar a instalação (ou seja, mais novos e compatíveis com o seu sitema). Em **Cargas de Trabalho**, selecione “Desenvolvimento para desktop com C++”. Instale as atualizações, feche o aplicativo e siga os próximos passos.

2. Siga todos os [passos usados no Linux](#em-linux), com exceção do item 3. Nele, o comando deve ser:
```console
.venv/Scripts/activate.bat
```
_Observação_: Nos comandos em Windows, o sentido da barra (`/` ou `\`) pode variar a depender da utilização de [WSL](https://learn.microsoft.com/pt-br/windows/wsl/about).

#### Utilizando WSL

Abra um novo terminal do Ubuntu e faça o clone do repositório forked do [querido-diario](https://github.com/okfn-brasil/querido-diario).

Siga as instruções referentes À instalação utilizando [Linux](CONTRIBUTING.md#em-linux).

[Este tutorial](https://github.com/Luisa-Coelho/qd-data-processing/blob/readme_update/wsl_windows.md) vai te ajudar na instalação e configuração do WSL na sua máquina Windows.


## Formação automática de código
O projeto usa [Black](https://github.com/psf/black) como ferramenta de automação para formatar e verificar o estilo do código e usa [isort](https://github.com/pycqa/isort) para organizar as importações. A integração contínua (CI) falhará se seu código não estiver adequadamente formatado.

Mas, se você seguiu as orientações para configurar o ambiente de desenvolvimento corretamente, especialmente instalando o `pre-commit`, é possível que você nunca precise corrigir a formatação manualmente. O `pre-commit` fará isso por você, já que executa antes de cada `commit`. Ainda, caso queira verificar todos os arquivos no projeto, use `make format` para evocar as ferramentas.

_Observação_: `make` não é disponibilizado nativamente em Windows, sendo necessário instalá-lo para a utilização sugerida.

# Mantendo
As pessoas mantenedoras devem seguir as diretrizes do [Guia para Mantenedoras](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#mantendo) do Querido Diário.

## Revisão de raspadores

Toda vez que uma PR para raspadores é aberta, a [lista de validações](https://github.com/okfn-brasil/querido-diario/blob/main/.github/pull_request_template.md) é acionada. É esperado que a pessoa contribuidora faça todas as verificações contidas na checklist, mas também é responsabilidade da pessoa revisora conferir os itens.

A checklist já cobre aspectos mais objetivos como o modelo do código, os campos obrigatórios e os arquivos de coleta-teste. Entretanto, outros aspectos devem ser levados em consideração na interação de revisão. Exemplos:

- Padrão de código Python quanto ao uso de aspas duplas (`"exemplo"` / `"exemplo='texto'"`)
- Boas práticas no uso do XPath ou seletores evitando "voltas" desnecessárias
- Legibilidade: se você teve dificuldade para entender algum trecho, verifique se este código pode ser melhorado
- Pense a interação de revisão como uma progressão da evolução da pessoa contribuidora junto ao projeto, dando *feedbacks* como comentários nas linhas necessárias e apontando questões gerais ou reforçando questões pontuais.
