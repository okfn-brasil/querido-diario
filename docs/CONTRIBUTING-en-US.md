**English (US)** | [Português (BR)](/docs/CONTRIBUTING.md)

# Contributing
Querido Diário has a [Contribution Guide](https://docs.queridodiario.ok.org.br/en/latest/contributing/contribution-guide.html#contributing) that is relevant to all of its repositories. The guide provides general information about how to interact with the project, the code of conduct you adhere to when contributing, the list of ecosystem repositories and the first actions you can take. We recommend reading it before continuing.

Already read? So let's go to the specific information of this repository:
- [Challenges](#challenges)
- [How to set up the development environment](#how-to-setup-the-development-environment)
    - [Linux](#linux)
    - [Windows](#windows)
- [Automated code formatting](#automated-code-formatting)
- [Maintaining](#maintaining)
    - [Scraper code review](#scraper-code-review)

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
#### Using Windows terminal
The following instructions were tried on Windows 10 and 11. Remember that if you want to integrate with the [querido-diario-data-processing](https://github.com/okfn-brasil/querido-diario- data-processing) it is preferable that your environment configuration is done [using WSL](CONTRIBUTING.md#using-wsl).

1. Install [Visual Studio Community](https://visualstudio.microsoft.com/pt-br/downloads/). Before the installation, you need to select in the **Individual Components** tab "Windows 10 SDK" or "11" (depending on your system) and "MSVC v143 build tools - VS 2022 C++ x64/x86 ( v14.32-17.4)". Note that Windows 10 SDK and MSVC v142 - VS 2019 C++ x64/x86 build tools versions will often be updated, so look for similar items under Individual Components to perform the installation (i.e. newer and compatible with your system). Under **Workloads**, select “Desktop development with C++”. Install the updates, close the application and follow the next steps.

2. Follow all [steps used in Linux](#linux), except for item 3. In it, the command should be:
```console
.venv/Scripts/activate.bat
```
_Note_: In Windows commands, the direction of the slash (`/` or `\`) may vary depending on the use of [WSL](https://learn.microsoft.com/en-us/windows/wsl/about).

#### Using WSL

Open a new Ubuntu terminal and clone the forked [querido-diario](https://github.com/okfn-brasil/querido-diario) repository 

Follow the instructions regarding installation using [Linux](CONTRIBUTING.md#em-linux).

[This tutorial](https://github.com/Luisa-Coelho/qd-data-processing/blob/readme_update/wsl_windows.md) will help you install and configure WSL on your Windows machine.

## Automated code formatting
Project uses [Black](https://github.com/psf/black) as an automated tool to format and check code style and [isort](https://github.com/pycqa/isort) to sort the imports. CI will fail if your code are not correctly formatted according these tools.

If you followed the setup instructions, installing pre-commit hooks, it is possible that you will never need to run these tools manually, as they will be execute before each commit. However, if you want to run them in all files in the project, you have `make format` command that will call these tools.

# Maintaining
Maintainers must follow the guidelines in Querido Diário's [Guide for Maintainers](https://docs.queridodiario.ok.org.br/en/latest/contributing/contribution-guide.html#maintaining).

## Scraper code review

Every time a PR for scrapers is opened, the [validation list](https://github.com/okfn-brasil/querido-diario/blob/main/.github/pull_request_template.md) is triggered. The contributing person is expected to carry out all the checks contained in the checklist, but it is also reviewer's responsibility to check them too.

The checklist already covers more objective aspects such as the code model, mandatory fields and test collection files. However, other aspects must be taken into consideration in the review interaction. Examples:

- Python code standard regarding the use of double quotes (`"example"` / `"example='texto'"`)
- Good practices in using XPath or selectors, avoiding unnecessary "turns"
- Readability: if you had difficulty understanding a section, check if this code can be improved
- Think review's interaction as a progression in the evolution of the person contributing to the project, giving *feedback* as comments on the necessary lines and pointing out general issues or reinforcing specific issues.
