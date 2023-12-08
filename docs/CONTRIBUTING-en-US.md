**English (US)** | [Português (BR)](/docs/CONTRIBUTING.md)

# Contributing
Querido Diário has a [Guide for Contributing](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#contribuindo) that is relevant to all of its repositories. The guide provides general information about how to interact with the project, the code of conduct you adhere to when contributing, the list of ecosystem repositories and the first actions you can take. We recommend reading it before continuing.

Already read? So let's go to the specific information of this repository:
- [Challenges](#challenges)
- [How to set up the development environment](#how-to-setup-the-development-environment)
    - [Linux](#linux)
    - [Windows](#windows)
- [Automated code formatting](#automated-code-formatting)
- [Maintaining](#maintaining)

## Challenges
The main challenge of this repository is to have more and more scrapers from websites that publish official gazettes, aiming to reach the 5570 Brazilian municipalities. We use the [City Expansion Board](https://github.com/orgs/okfn-brasil/projects/12/views/13) to organize this challenge progress. Consult it to find relevant tasks you can contribute to.

To help you develop, use the guidelines on the page about [how to write a new scraper](https://docs.queridodiario.ok.org.br/en/latest/writing-a-new-spider.html) available at [Querido Diario's technical documentation](https://docs.queridodiario.ok.org.br/en/latest/).

## How to setup the development environment
Scrapers are developed using [Python](https://docs.python.org/3/) and [Scrapy](https://scrapy.org) framework. You can check [how to install Python](https://www.python.org/downloads/) on your operating system and learn more about Scrapy [in this tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html). With Python on your computer, follow the development environment setup step-by-step:

### Linux
1. Create a fork of this repository and, with a terminal open in a preferred directory on your computer, clone it and access the new directory created with the name of the repository.
``` console
git clone <repository_fork>
cd querido-diario
```
2. Create a new [virtual environment](https://docs.python.org/3/library/venv.html) which will keep the project isolated from your system.
``` console
python3 -m venv .venv
```
3. Activate the newly created virtual environment
``` console
source .venv/bin/activate
```
4. Install the [required libraries](querido-diario/data_collection/requirements-dev.txt).
``` console
pip install -r data_collection/requirements-dev.txt
```
5. Install pre-commit, a tool that verifies if code attends project standards when _committing_.
``` console
pre-commit install
```
6. Your development environment is ready! :tada:

_Attention:_ These steps need to be executed only the first time you interact with the project during the environment setup. After that, just activate the virtual environment (step 3) every time you use or contribute to the repository.

### Windows
The following instructions were tried on Windows 10.
1. [Install Microsoft Visual Build Tools](https://visualstudio.microsoft.com/downloads/). When starting the installation, you need to select `C++ build tools` in the loading tab and also `Windows 10 SDK` and `MSVC v142 - VS 2019 C++ x64/x86 build tools` in the individual components tab.
2. Follow all [steps used in Linux](#linux), except for item 3. In it, the command should be:
```console
.venv/Scripts/activate.bat
```
_Note_: In Windows commands, the direction of the slash (`/` or `\`) may vary depending on the use of [WSL](https://learn.microsoft.com/en-us/windows/wsl/about).

## Automated code formatting
Project uses [Black](https://github.com/psf/black) as an automated tool to format and check code style and [isort](https://github.com/pycqa/isort) to sort the imports. CI will fail if your code are not correctly formatted according these tools.

If you followed the setup instructions, installing pre-commit hooks, it is possible that you will never need to run these tools manually, as they will be execute before each commit. However, if you want to run them in all files in the project, you have `make format` command that will call these tools.

# Maintaining
Maintainers must follow the guidelines in Querido Diário's [Guide for Maintainers](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING-en-US.md#maintaining).
