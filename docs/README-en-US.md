**English (US)** | [Português (BR)](/docs/README.md)

<p align="center">
  <a href="https://queridodiario.ok.org.br/sobre" target="_blank"> <img alt="Querido Diário" src="./images/querido-diario-logo.png" width="200">
  </a>
</p>

# Querido Diário
Within the [Querido Diário ecosystem](https://docs.queridodiario.ok.org.br/en/latest/contributing/contribution-guide.html#ecosystem), this repository is responsible for **scraping official gazettes publishing sites**

Find out more about [technologies](https://queridodiario.ok.org.br/tecnologia) and [history](https://queridodiario.ok.org.br/sobre) of the project on the [Querido Diário website](https://queridodiario.ok.org.br)

# Summary
- [How to contribute](#how-to-contribute)
- [Development Environment](#development-environment)
- [How to run](#how-to-run)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [Thanks](#thanks)
- [Open Knowledge Brazil](#open-knowledge-brazil)
- [License](#license)

# How to contribute
<p>  
  <a href="https://www.catarse.me/queridodiario-okbr" target="_blank"> 
    <img alt="catarse" src="https://img.shields.io/badge/Catarse-Apoie%20o%20projeto-orange?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDMyNSA0NTUiIHdpZHRoPSIzMjUiIGhlaWdodD0iNDU1Ij4KCTx0aXRsZT5sb2dvLXYtY29yLXBvc2l0aXZvLWFpPC90aXRsZT4KCTxzdHlsZT4KCQkuczAgeyBmaWxsOiAjMTdhMzM4IH0gCgkJLnMxIHsgZmlsbDogIzdkYjkzZCB9IAoJCS5zMiB7IGZpbGw6ICNmMmJmMDAgfSAKCQkuczMgeyBmaWxsOiAjZjE5MTA2IH0gCgkJLnM0IHsgZmlsbDogI2VhNjYwYiB9IAoJCS5zNSB7IGZpbGw6ICNkZTMyODEgfSAKCTwvc3R5bGU+Cgk8ZyBpZD0iTGF5ZXIgMSI+CgkJPGcgaWQ9IiZsdDtHcm91cCZndDsiPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczAiIGQ9Im01Ni40IDI1Ni40cS0xLjggMy4xLTMuNCA2LjRjLTE1LjQgMzMuMS00LjcgNjMuMSAxNC44IDkyLjQgMTEuNiAxNy40IDguNiAzNi40LTEuOSA0Ny4zLTYgNi4zLTE0LjUgOS44LTIzLjIgOS43LTQuNSAwLTkuMS0wLjktMTMuNS0zLTYuMy0yLjktMTUuMS05LjEtMjIuMi0yOC43LTguOS0yNC4yLTkuMS01MS42IDIuNi03Ni44IDEwLjEtMjEuNiAyNi45LTM3LjggNDYuOC00Ny4zeiIvPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczEiIGQ9Im00Ni41IDMwNS44YzAuNSAyLjYgMSA1LjIgMS43IDcuOCAxMC41IDM4LjcgNDAuNyA1Ni41IDc3LjggNjcuNCAyMi4xIDYuNSAzMyAyNC43IDMxLjkgNDEuMi0wLjcgOS42LTUuMyAxOC41LTEyLjcgMjQuNi0zLjggMy4yLTguNCA1LjctMTMuNSA3LTcuNCAyLTE5LjIgMy0zOS4xLTguNC0yNC41LTE0LjItNDQuMS0zNy4yLTUyLTY2LjctNi44LTI1LjItNC4xLTUwLjggNS45LTcyLjl6Ii8+CgkJCTxwYXRoIGlkPSImbHQ7UGF0aCZndDsiIGNsYXNzPSJzMiIgZD0ibTczLjIgMzU0LjVjMi4yIDEuOCA0LjUgMy42IDYuOSA1LjMgMzYuMiAyNS4zIDc0LjMgMTguOSAxMTMuMiAxLjggMjMuMi0xMC4xIDQ1LjMtMi41IDU2IDEyLjIgNi4zIDguNiA4LjYgMTkuNCA2LjggMjkuNy0xIDUuNC0zLjEgMTAuNy02LjUgMTUuNS00LjggNi45LTE0IDE2LjEtMzguOSAyMC41LTMwLjcgNS40LTYzLjQtMC4xLTkwLjktMTkuNC0yMy42LTE2LjUtMzkuNC0zOS45LTQ2LjYtNjUuNnoiLz4KCQkJPHBhdGggaWQ9IiZsdDtQYXRoJmd0OyIgY2xhc3M9InMzIiBkPSJtMTMwLjEgMzc2LjZxNC43IDAuMSA5LjUtMC40YzQ4LjQtNC4zIDc2LTM2LjUgOTYuNy03OC41IDEyLjQtMjUgMzYuNC0zNC4xIDU1LjgtMjkuMyAxMS40IDIuOCAyMSAxMC4yIDI2LjcgMjAuMyAzIDUuMiA1IDExLjEgNS41IDE3LjYgMC45IDkuMi0wLjQgMjMuNC0xOC4zIDQ0LjctMjIgMjYuMy01My41IDQ0LjgtOTAuMyA0OC0zMS41IDIuOC02MS40LTUuOC04NS42LTIyLjR6Ii8+CgkJCTxwYXRoIGlkPSImbHQ7UGF0aCZndDsiIGNsYXNzPSJzNCIgZD0ibTE5My42IDM1NS4xYzIuNy0yLjIgNS4zLTQuNiA3LjgtNy4xIDM3LjctMzcuOCAzOC4xLTg0LjUgMjUuOS0xMzQuNS03LjItMjkuOCA2LjUtNTQuNSAyNi4zLTY0LjIgMTEuNS01LjYgMjQuOS02LjEgMzYuOC0xLjggNi4zIDIuMyAxMi4xIDUuOSAxNy4xIDExIDcuMiA3LjEgMTYuMiAyMC4xIDE2LjMgNTAuNiAwIDM3LjctMTMuNSA3NS42LTQyLjIgMTA0LjMtMjQuNiAyNC43LTU1LjkgMzguNi04OCA0MS43eiIvPgoJCQk8cGF0aCBpZD0iJmx0O1BhdGgmZ3Q7IiBjbGFzcz0iczUiIGQ9Im0yMzEuOSAyOTJjMC44LTQuNCAxLjQtOC45IDEuOC0xMy41IDYtNjkuMi0zMi42LTExNi04Ni41LTE1NS43LTMyLjItMjMuNi0zOS4xLTU5LjYtMjcuNS04NS44IDYuNy0xNS4zIDE5LjctMjcgMzUuMi0zMi42IDguMS0yLjkgMTctNC4yIDI2LjEtMy40IDEzLjIgMS4xIDMzIDYuNSA1OC42IDM2LjkgMzEuNSAzNy41IDQ5LjcgODYuNSA0NS4xIDEzOS4xLTMuOSA0NS4xLTIzLjQgODUuMS01Mi44IDExNXoiLz4KCQk8L2c+Cgk8L2c+Cjwvc3ZnPg==">
  </a>
</p> 

Thank you for considering contributing to Querido Diário! :tada:

You can find how to do it at [CONTRIBUTING-en-US.md](/docs/CONTRIBUTING-en-US.md)!

Also, check the [Querido Diário documentation](https://docs.queridodiario.ok.org.br/en/latest/) to help you.

# Development Environment
You need to have [Python](https://docs.python.org/3/) (+3.0) and [Scrapy](https://scrapy.org) framework installed.

The commands below set it up in Linux operating system. They consist of creating a [virtual Python environment](https://docs.python.org/3/library/venv.html), installing the requirements listed in `requirements-dev` and the code standardization tool `pre-commit`.

``` console
python3 -m venv .venv
source .venv/bin/activate
pip install -r data_collection/requirements-dev.txt
pre-commit install
```

> Configuration on other operating systems is available at ["how to setup the development environment"](/docs/CONTRIBUTING-en-US.md#how-to-setup-the-development-environment), including more details for those who want to contribute to the repository.

# How to run
To try running a scraper already integrated into the project or to test what you are developing, follow the commands:

1. If you haven't already done so, activate the virtual environment in the `/querido-diario` directory:
``` console
source .venv/bin/activate
```
2. Go to the `data_collection` directory:
```console
cd data_collection
```
3. Check the available scrapers list:
```console
scrapy list
```
4. Run a listed scraper:
```console
scrapy crawl <scraper_name> //example: scrapy crawl ba_acajutiba
```
5. The official gazettes collected from scraping will be saved in the `data_collection/data` folder

6. When executing item 4, the scraper will collect all official gazettes from the publishing site of that municipality since the first digital edition. For smaller runs, use flags in the run command:

- `start_date=YYYY-MM-DD`: will set the collecting start date.
```console
scrapy crawl <scraper_name> -a start_date=<YYYY-MM-DD>
```
- `end_date=YYYY-MM-DD`: will set the collecting end date. If omitted, it will assume the date of the day it is being executed.
```console
scrapy crawl <scraper_name> -a end_date=<YYYY-MM-DD>
```

# Troubleshooting
Check out the [troubleshooting](/docs/TROUBLESHOOTING-en-US.md) file to resolve the most common issues with project environment setup.

# Support
<p>
  <a href="https://go.ok.org.br/discord" target="_blank">
    <img alt="Discord Invite" src="https://img.shields.io/badge/Discord-Entre%20no%20servidor-blue?style=for-the-badge&logo=discord" >
  </a>
</p>

Join our [community server](https://go.ok.org.br/discord) for exchanges about projects, questions, requests for help with contributions and talk about civic innovation in general.

# Thanks
This project is maintained by Open Knowledge Brazil and made possible thanks to the technical communities, the [Ambassadors of Civic Innovation](https://embaixadoras.ok.org.br/), volunteers and financial donors, in addition to partner universities, companies supporters and funders.

Meet [who supports Querido Diario](https://queridodiario.ok.org.br/apoie#quem-apoia).

# Open Knowledge Brazil
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
</p>

[Open Knowledge Brazil](https://ok.org.br/) is a non-profit civil society organization whose mission is to use and develop civic tools, projects, public policy analysis and data journalism to promote free knowledge in the various fields of society.

All work produced by OKBR is openly and freely available.

# License

Code licensed under the [MIT License](/LICENSE.md).
