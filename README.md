**Português (BR)** | [English (US)](.github/README-en-US.md) 

<p align="center">
  <a href="https://queridodiario.ok.org.br/sobre" target="_blank"> <img alt="Querido Diário" src="./.github/images/querido-diario-logo.png" width="200">
  </a>
</p>

# Querido Diário
Dentro do [ecossistema do Querido Diário](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#ecossistema), este repositório é o responsável pela tarefa de **raspagem dos sites publicadores de diários**.

Conheça mais sobre as [tecnologias](https://queridodiario.ok.org.br/tecnologia) e a [história](https://queridodiario.ok.org.br/sobre) do projeto no [site do Querido Diário](https://queridodiario.ok.org.br)

# Sumário
- [Como contribuir](#como-contribuir)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
  - [Em Linux](#em-linux)
  - [Em MacOS](#em-macos)
  - [Em Windows](#em-windows)
- [Como executar](#como-executar)
- [Solução de problemas](#solução-de-problemas)
- [Suporte](#suporte)
- [Agradecimentos](#agradecimentos)
- [Open Knowledge Brasil](#open-knowledge-brasil)
- [Licença](#licença)

# Como contribuir
<p>  
  <a href="https://www.catarse.me/queridodiario-okbr" target="_blank"> 
    <img alt="catarse" src="https://img.shields.io/badge/Catarse-Apoie o projeto-orange?style=for-the-badge&logo=data:image/ico;base64,AAABAAEAEBIAAAEAIAAXAgAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEggGAAAAUjteagAAAd5JREFUOI2NlLFrU1EUh7/z7mtIQiWh1ae0SKJBxBaxzyUgBUsULOjQoeCm6V9g1cVB8AUXwSFxcRBB+gYRB3Vw0Mk4OAhCsuiiKVFEsBFqwYJJTa5Dk9fXlzTNb7r33PP77jmcyxWtNSJCUBXbmQIKwGngK5BNlZwigNbayzO6nFt60TYDJIA3FdvJBpP6ARI9YoWK7SQHBZR7xGKAMyhgAaj2iF9ePpmL7wpIlZwyYAPF4Jk5+nG+s5adpuBXxXYeAdnOPnL0CWrPt6vWg/VCvxb81SyIanzxblV/ARb7thCUGv5+f9Ncx4iuQHtKAwMSRTcPMLT/QydU3gaw3PSc5abj3dYthcbeeQBRPPUAlpueAZ6vXHr/ezeAqDoS1gwd2Tjvr6AwagoXnp2a3slcuxa5A2yax5uIYtIPODEWEsZDstTL/OtG+CJNrpsHmoSS/5CwBrgHYLZzqvUWyX2mHH74euLTpKo9njBqL/UPNUODWf40z9DycgGc2JVGzl/BUrXeoqHRq0SPpYzV20BJIjoPnCOqTYY17G0BHIovbuQ6JO8lWm56an7EPDtiyl1L1smoZQ4aa8FuyrEMtv8/6HrKN19NzwG3gORx42d+1vy8BsSBYizDW9j+ofwHqM6MbbvUDjEAAAAASUVORK5CYII=">
  </a>
</p> 

Agradecemos por considerar contribuir com o Querido Diário! :tada:

Você encontra como fazê-lo no [CONTRIBUTING.md](.github/CONTRIBUTING.md)!

# Como configurar o ambiente de desenvolvimento
Os raspadores são desenvolvidos usando [Python](https://docs.python.org/3/) e o framework [Scrapy](https://scrapy.org). Você pode conferir como [instalar Python](https://www.python.org/downloads/) e como [instalar Scrapy](https://docs.scrapy.org/en/latest/intro/install.html#installing-scrapy) em seu sistema operacional.

Com ambos prontos em seu computador, siga o passo-a-passo da configuração do ambiente de desenvolvimento:

## Em Linux
1. Faça um fork deste repositório e, com o terminal aberto em um diretório de preferência no seu computador, clone-o e acesse o novo diretório criado com o nome do repositório.
``` console
$ git clone <endereço_copiado_do_código_do_fork>
$ cd querido-diario
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
Depois de configurar o ambiente de desenvolvimento, você poderá desenvolver e executar novos raspadores. 

1. Se ainda não o fez, ative o ambiente virtual no diretório `/querido-diario`:
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

# Solução de problemas

## `Python.h` faltando

Ao rodar o comando `pip install`, você pode obter o seguinte erro:

```
module.c:1:10: fatal error: Python.h: No such file or directory
     #include <Python.h>
              ^~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```
Tente instalar `python3-dev`. Por exemplo, via `apt install python3-dev`, se você está usando uma distro Debian, ou utilize o gerenciamento de pacotes da sua distro (por exemplo, `python3.6-dev` or `python3.7-dev`). Você pode saber qual é a sua versão via `python3 --version`.

# Suporte 
<p>  
  <a href="https://discord.com/invite/mxHGPq8rdY" target="_blank">
    <img alt="Discord Invite" src="https://img.shields.io/badge/Discord-Entre%20no%20servidor-blue?style=for-the-badge&logo=discord" >
  </a>
</p>

Ingresse em nosso [Discord](https://discord.com/invite/mxHGPq8rdY) para trocas sobre os projetos, dúvidas, pedidos de ajuda com contribuição e conversar sobre inovação cívica em geral. 

# Agradecimentos
Este projeto é mantido pela Open Knowledge Brasil e possível graças à comunidade técnica, às [Embaixadoras de Inovação Cívica](https://embaixadoras.ok.org.br/), às pessoas voluntárias e doadoras financeiras, além de universidades parceiras, empresas apoiadoras e financiadoras.

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
  <a href="https://www.facebook.com/OpenKnowledgeBrasil" target="_blank">
    <img alt="Facebook Follow" src="https://img.shields.io/badge/Facebook-_-informational?style=for-the-badge&logo=facebook">
  </a>
</p>

A [Open Knowledge Brasil](https://ok.org.br/) é uma organização da sociedade civil sem fins lucrativos, cuja missão é utilizar e desenvolver ferramentas cívicas, projetos, análises de políticas públicas, jornalismo de dados para promover o conhecimento livre nos diversos campos da sociedade.

Todo o trabalho produzido pela OKBR está disponível livremente.

# Licença

Código licenciado sob a [Licença MIT](LICENSE.md).
