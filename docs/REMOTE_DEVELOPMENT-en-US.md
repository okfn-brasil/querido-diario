**English (US)** | [Português (BR)](REMOTE_DEVELOPMENT.md)

# Remote development with GitHub Codespaces

For workshops or a first contribution, GitHub Codespaces lets you edit and run
the scrapers in a browser. This repository includes a development container with
Python 3.13 and uv. It installs the locked project dependencies, development
tools, and pre-commit hooks when the codespace is created.

## Create the environment

1. Fork the repository. Make sure your branch contains the `.devcontainer` folder.
2. Check your [included Codespaces usage and billing settings](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).
   Included usage and availability depend on your account; do not assume unlimited
   free access. A local [VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)
   uses the same configuration if you already have Docker installed.
3. On your fork, select **Code → Codespaces → Create codespace** for your branch.
4. Wait for the container build and `postCreateCommand` to finish. If setup fails,
   inspect the creation log rather than continuing with a partial environment.
5. Open a terminal at the repository root and check the environment:

   ```console
   cd querido_diario_raspadores
   uv run python --version
   uv run scrapy list
   uv run pytest tests/ -q
   ```

The container configuration lives in [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json).
After changing it, run **Codespaces: Rebuild Container** from the command palette.
To retry dependency setup manually, run `uv sync --all-groups --locked` from
`querido_diario_raspadores`.

## Collect a small sample and download the evidence

From `querido_diario_raspadores`, run an existing scraper over a short interval:

```console
uv run scrapy crawl sp_adolfo -a start=2024-03-01 -a end=2024-03-05 -O sample.csv -s LOG_FILE=sample.log
```

Downloaded gazettes are under `querido_diario_raspadores/data/3500204/`.
The CSV and log are in `querido_diario_raspadores`. Open them in the Explorer,
check that the dates and files match, and use **Download** from the file context
menu to save the evidence to your computer. Open downloaded PDFs to confirm they
contain gazettes. Follow the [PR checklist](../.github/pull_request_template.md)
for all collection checks required for your contribution.

The default setup stores files and the SQLite database locally inside the
codespace. It does not require AWS, Zyte, or production API credentials for this
sample. Some publishers restrict access by location, so a website reachable on
your computer may fail from a codespace.

## Finish your session

Commit and push work you want to keep to your fork, and download collection
evidence before deleting the environment. Stop the codespace when you finish;
stopped codespaces still use storage. Delete it from
[your codespaces](https://github.com/codespaces) when it is no longer needed.

## Evaluation scope

This configuration can also be built and checked locally with Docker. A local
container check verifies the Linux dependency installation and project commands,
but does not verify hosted Codespaces creation, browser file downloads, account
quotas, or publisher access from GitHub's network. Record those results separately
when evaluating Codespaces for [issue #1294](https://github.com/okfn-brasil/querido-diario/issues/1294).
