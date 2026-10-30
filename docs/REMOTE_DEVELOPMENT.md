**Português (BR)** | [English (US)](REMOTE_DEVELOPMENT-en-US.md)

# Desenvolvimento remoto com GitHub Codespaces

Para oficinas ou uma primeira contribuição, o GitHub Codespaces permite editar e
executar os raspadores pelo navegador. Este repositório inclui um contêiner de
desenvolvimento com Python 3.13 e uv. Ao criar o codespace, ele instala as
dependências do arquivo de lock, as ferramentas de desenvolvimento e os hooks do
pre-commit.

## Criando o ambiente

1. Faça um fork do repositório. Confira se a sua branch contém a pasta `.devcontainer`.
2. Confira seu [uso incluído e as configurações de cobrança do Codespaces](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).
   A disponibilidade e o uso incluído dependem da sua conta; não presuma acesso
   gratuito ilimitado. Um [Dev Container local no VS Code](https://code.visualstudio.com/docs/devcontainers/containers)
   usa a mesma configuração se você já tem o Docker instalado.
3. No seu fork, selecione **Code → Codespaces → Create codespace** na sua branch.
4. Aguarde a construção do contêiner e o término do `postCreateCommand`. Se a
   configuração falhar, consulte o log de criação antes de continuar.
5. Abra um terminal na raiz do repositório e confira o ambiente:

   ```console
   cd querido_diario_raspadores
   uv run python --version
   uv run scrapy list
   uv run pytest tests/ -q
   ```

A configuração está em [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json).
Após alterá-la, execute **Codespaces: Rebuild Container** na paleta de comandos.
Para repetir a instalação das dependências manualmente, execute
`uv sync --all-groups --locked` em `querido_diario_raspadores`.

## Coletando uma amostra e baixando os arquivos de teste

Em `querido_diario_raspadores`, execute um raspador existente em um intervalo curto:

```console
uv run scrapy crawl sp_adolfo -a start=2024-03-01 -a end=2024-03-05 -O sample.csv -s LOG_FILE=sample.log
```

Os diários baixados ficam em `querido_diario_raspadores/data/3500204/`.
O CSV e o log ficam em `querido_diario_raspadores`. Abra-os no Explorer,
confira as datas e os arquivos coletados e use **Download** no menu de contexto
dos arquivos para salvá-los no seu computador. Abra os PDFs para confirmar que
contêm diários oficiais. Siga a [checklist de PR](../.github/pull_request_template.md)
para todas as verificações de coleta exigidas para a sua contribuição.

A configuração padrão armazena os arquivos e o banco SQLite localmente no
codespace. Essa amostra não exige credenciais da AWS, do Zyte ou da API de
produção. Alguns publicadores restringem o acesso por localização; um site
acessível no seu computador pode falhar a partir de um codespace.

## Encerrando a sessão

Faça commit e push do trabalho que deseja manter para o seu fork e baixe os
arquivos de teste antes de excluir o ambiente. Pare o codespace ao terminar;
codespaces parados ainda consomem armazenamento. Exclua-o na página
[dos seus codespaces](https://github.com/codespaces) quando não precisar mais dele.

## Escopo da avaliação

Essa configuração também pode ser construída e verificada localmente com Docker.
Uma verificação local valida a instalação das dependências em Linux e os comandos
do projeto, mas não valida a criação no Codespaces hospedado, os downloads pelo
navegador, as cotas da conta ou o acesso aos publicadores pela rede do GitHub.
Registre esses resultados separadamente ao avaliar o Codespaces para a
[issue #1294](https://github.com/okfn-brasil/querido-diario/issues/1294).
