**Português (BR)** | [English (US)](/docs/CONTRIBUTING-en-US.md)

# Contribuindo
O Querido Diário possui um [Guia para Contribuição](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#contribuindo) principal que é relevante para todos os seus repositórios. Este guia traz informações gerais sobre como interagir com o projeto, o código de conduta que você adere ao contribuir, a lista de repositórios do ecossistema e as primeiras ações que você pode tomar. Recomendamos sua leitura antes de continuar.

Já leu? Então vamos às informações específicas deste repositório:
- [Desafios](#desafios)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
    - [Em Linux](#em-linux)
    - [Em Windows](#em-windows)
- [Formatação automática de código](#formação-automática-de-código)
- [Mantendo](#mantendo)

## Desafios
O principal desafio deste repositório é ter cada vez mais raspadores de sites publicadores de diários oficiais, visando atingir os 5570 municípios brasileiros. Utilizamos o [Quadro de Expansão de Cidades](https://github.com/orgs/okfn-brasil/projects/12/views/13) para organizar o progresso do desafio. Consulte-o para localizar tarefas relevantes com as quais você pode contribuir. 

Para te ajudar a desenvolver, utilize as orientações da página sobre [como escrever um novo raspador](https://docs.queridodiario.ok.org.br/pt-br/latest/escrevendo-um-novo-spider.html) disponível na [documentação técnica do Querido Diário](https://docs.queridodiario.ok.org.br/pt-br/latest/).

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
As instruções a seguir foram experimentadas em Windows 10. 
1. [Instale o Microsoft Visual Build Tools](https://visualstudio.microsoft.com/downloads/). Ao iniciar a instalação, você precisa selecionar `C++ build tools` na aba de carregamento e também `Windows 10 SDK` e `MSVC v142 - VS 2019 C++ x64/x86 build tools` na aba de componentes individuais.
2. Siga todos os [passos usados no Linux](#em-linux), com exceção do item 3. Nele, o comando deve ser:
```console
.venv/Scripts/activate.bat
```
_Observação_: Nos comandos em Windows, o sentido da barra (`/` ou `\`) pode variar a depender da utilização de [WSL](https://learn.microsoft.com/pt-br/windows/wsl/about).

## Formação automática de código
O projeto usa [Black](https://github.com/psf/black) como ferramenta de automação para formatar e verificar o estilo do código e usa [isort](https://github.com/pycqa/isort) para organizar as importações. A integração contínua (CI) falhará se seu código não estiver adequadamente formatado. 

Mas, se você seguiu as orientações para configurar o ambiente de desenvolvimento corretamente, especialmente instalando o `pre-commit`, é possível que você nunca precise corrigir a formatação manualmente. O `pre-commit` fará isso por você, já que executa antes de cada `commit`. Ainda, caso queira verificar todos os arquivos no projeto, use `make format` para evocar as ferramentas.

_Observação_: `make` não é disponibilizado nativamente em Windows, sendo necessário instalá-lo para a utilização sugerida.

# Mantendo
As pessoas mantenedoras devem seguir as diretrizes do [Guia para Mantenedoras](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#mantendo) do Querido Diário.