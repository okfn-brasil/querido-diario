**Português (BR)** | [English (US)](.github/README-en-US.md) | [Español](.github/README-es.md)

<p align="center">
  <a href="https://queridodiario.ok.org.br/sobre" target="_blank"> <img alt="Querido Diário" src="./.github/images/querido-diario-logo.png" width="200">
  </a>
</p>

# Querido Diário
Dentro do [ecossistema do Querido Diário](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#ecossistema), este repositório é o responsável pela tarefa de **raspagem dos sites publicadores de diários**.

Conheça mais sobre as [tecnologias](https://queridodiario.ok.org.br/tecnologia) e a [história](https://queridodiario.ok.org.br/sobre) do projeto no [site do Querido Diário](https://queridodiario.ok.org.br)

# Sumário
- [Contribua](#contribua)
- [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
  - [Em Linux](#em-linux)
  - [Em MacOS](#em-macos)
  - [Em Windows](#em-windows)
- [Como executar](#como-executar)
- [Agradecimentos](#agradecimentos)
- [Open Knowledge Brasil](#open-knowledge-brasil)
- [Licença](#licença)

# Contribua
<p>
  <a href="https://discord.com/invite/aC3Q33q" target="_blank">
    <img alt="Discord Invite" src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" width="100">
  </a>
  <a href="https://www.catarse.me/projects/120548/" target="_blank">
    <img alt="catarse" src="https://img.shields.io/badge/Doe-Catarse-green" width="100">
  </a>
</p>

Está interessado(a) em contribuir para o repositório? :tada:
Comece lendo o **[Guia de Contribuição](.github/CONTRIBUTING.md)**!

# Ambiente de desenvolvimento
Os raspadores são desenvolvidos usando [Python](https://docs.python.org/3/) e o framework [Scrapy](https://scrapy.org). Você pode conferir como [instalar Python](https://www.python.org/downloads/) e como [instalar Scrapy](https://docs.scrapy.org/en/latest/intro/install.html#installing-scrapy) em seu sistema operacional.

Com ambos prontos em seu computador, siga o passo-a-passo da configuração do ambiente de desenvolvimento:

## Em Linux
1. Faça um fork deste repositório e, com o terminal aberto em um diretório de preferência no seu computador, clone-o.
``` console
$ git clone <endereço_copiado_do_código_do_fork>
```

2. Crie um novo [ambiente virtual](https://docs.python.org/pt-br/3/library/venv.html) - que manterá as execuções do projeto isoladas de seu sistema.
``` console
$ python3 -m venv .venv
```

3. Ative o recém criado ambiente virtual
``` console
$ source .venv/bin/activate
```

4. Instale as bibliotecas requeridas pelo projeto.
``` console
$ pip install -r data_collection/requirements-dev.txt
```

5. Instale o pré-commit, uma ferramenta que, ao fazer o _commit_ do código, verifica se ele se adequa aos padrões do projeto.
``` console
$ pre-commit install
```

6. Seu ambiente de desenvolvimento está pronto! :tada:

_Observação:_ Estas etapas precisam ser executadas apenas na primeira vez que interagir com o projeto, durante a preparação do ambiente. Depois disso, basta ativar o ambiente virtual (passo 3) cada vez que for utilizar ou contribuir com o repositório.

## Em MacOS
[_em construção_]

## Em Windows
1. [Instale o Microsoft Visual Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/). Ao iniciar a instalação, você precisa selecionar `C++ build tools` na aba de carregamento e também `Windows 10 SDK` e `MSVC v142 - VS 2019 C++ x64/x86 build tools` na aba de componentes individuais.

2. Siga todos os [passos usados no Linux](#em-linux), com exceção do item 3. Nele, o comando deve ser:
```console
$ .venv/Scripts/activate.bat
```

# Como executar
Depois de configurar o ambiente de desenvolvimento, você poderá desenvolver e executar novos raspadores. As instruções a seguir servem para Linux, MacOs e Windows.

1. Se ainda não o fez, ative o ambiente virtual:
``` console
$ source .venv/bin/activate
```

2. Vá para o diretório `data_collection`:
```console
$ cd data_collection
```
3. Verifique a lista de raspadores disponíveis:
```console
$ scrapy list
```
4. Execute um raspador da lista:
```console
$ scrapy crawl <nome_do_raspador>
```

5. Os diários coletados na raspagem serão salvos na pasta `data_collection/data`

6. Ao executar o item 4, o raspador coletará todos os diários oficiais do site publicador daquele município desde a primeira edição digital. Para execuções menores, utilize flags no comando de execução:

a. `start_date=AAAA-MM-DD`: definirá a data inicial de coleta de diários.
```console
$ scrapy crawl <nome_do_raspador> -a start_date=<AAAA-MM-DD>
```

# Agradecimentos
Este projeto é mantido pela Open Knowledge Brasil e possível graças a comunidade técnica, as [Embaixadoras de Inovação Cívica](https://embaixadoras.ok.org.br/), voluntárias, doadoras financeiras, além de universidades parceiras, empresas apoiadoras e financiadoras. Saiba quem são na [página de apoio do Querido Diário](https://queridodiario.ok.org.br/apoie#quem-apoia)

# Open Knowledge Brasil
<p>
  <a href="https://twitter.com/okfnbr" target="_blank">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" width="100">
  </a>
  <a href="https://www.instagram.com/openknowledgebrasil/" target="_blank">
    <img alt="Instagram Follow" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" width="110">
  </a>
  <a href="https://www.linkedin.com/company/open-knowledge-brasil" target="_blank">
    <img alt="LinkedIn Follow" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="100">
  </a>
  <a href="https://www.facebook.com/OpenKnowledgeBrasil" target="_blank">
    <img alt="Facebook Follow" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" width="105">
  </a>
</p>

A [Open Knowledge Brasil](https://ok.org.br/) é uma organização da sociedade civil sem fins lucrativos, cuja missão é utilizar e desenvolver ferramentas cívicas, projetos, análises de políticas públicas, jornalismo de dados para promover o conhecimento livre nos diversos campos da sociedade.

Todo o trabalho produzido pela OKBR está disponível livremente.

# Licença

Código licenciado sob a [Licença MIT](LICENSE.md).
