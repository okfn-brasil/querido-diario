**Português (BR)** | [English (US)](/docs/CONTRIBUTING-en-US.md)

# Contribuindo
O Querido Diário possui um [Guia para Contribuição](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#contribuindo) principal que é relevante para todos os seus repositórios. Este guia traz informações gerais sobre como interagir com o projeto, o código de conduta que você adere ao contribuir, a lista de repositórios do ecossistema e as primeiras ações que você pode tomar. Recomendamos sua leitura antes de continuar.

Já leu? Então vamos às informações específicas deste repositório:
- [Desafios](#desafios)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
- [Desafios](#desafios)
    - [Labels](#labels)
    - [Metas do Repositório](#metas-do-repositório)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
    - [Em Linux](#em-linux)
    - [Em Windows](#em-windows)
  - [Formatação automática de código](#formação-automática-de-código)
- [Mantendo](#mantendo)
    - [Revisão de raspadores](#revisão-de-raspadores)

## Desafios
O principal desafio deste repositório é ter cada vez mais raspadores de sites publicadores de diários oficiais, visando atingir os 5570 municípios brasileiros. Utilizamos o [Quadro de Expansão de Cidades](https://github.com/orgs/okfn-brasil/projects/12/views/13) para organizar o progresso do desafio. Consulte-o para localizar tarefas relevantes com as quais você pode contribuir.

Para te ajudar a desenvolver, utilize as orientações da página ["contrbuindo com raspadores"](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#contribuindo-com-raspadores) disponível na [documentação técnica do Querido Diário](https://docs.queridodiario.ok.org.br/).


### Labels
As issues são marcadas com etiquetas, um recurso que serve para classificar issues de mesmo tipo, sinalizar se há algum empecilho ou direcionar a comunidade para tarefas mais do perfil delas. No geral, adotamos *labels* comuns a outros projetos de código aberto como "docs", "bug", "dependencies", mas também temos algumas específicas. Veja quais são na seção de [labels](https://github.com/okfn-brasil/querido-diario/labels)


### Metas do Repositório
Para garantir que nossos esforços estejam alinhados e focados em objetivos claros, definimos metas para o desenvolvimento e expansão do projeto. Estas metas são revisadas e atualizadas regularmente, refletindo as prioridades e os desafios que enfrentamos. Convidamos as pessoas contribuidoras a se familiarizarem com estas metas, disponíveis em nosso [Quadro de Metas](https://github.com/okfn-brasil/querido-diario/milestones). Sua contribuição pode ser ainda mais valiosa quando alinhada com estas direções.


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
4. Instale as [bibliotecas requeridas](querido-diario/data_collection/requirements-dev.txt).
``` console
pip install -r data_collection/requirements-dev.txt
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
