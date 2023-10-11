# Define cores para o terminal.
BOLD := $(shell tput bold)
RED := $(shell tput -Txterm setaf 1)
GREEN := $(shell tput -Txterm setaf 2)
BLUE := $(shell tput -Txterm setaf 6)
RESET := $(shell tput -Txterm sgr0)

# Define argumentos do isort
ISORT_ARGS := --combine-star --combine-as --order-by-type --thirdparty scrapy --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

# Define diretório de dados.
SRC_DIRS := ./data_collection

# Define o nome do ambiente virtual.
VENV_DIR = $(shell pwd)/.venv/bin/activate

# Proteção contra comandos que possam ter o mesmo nome de variáveis
.PHONY: all help check format run_spider sql clean shell run_spider_since compile install

all: install

help: ## Mostra ajuda para os comandos do Makefile.
	@echo "$(BOLD)$(BLUE)Comandos disponíveis:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "$(BOLD)$(GREEN)%-20s$(RESET)%s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: .venv/bin/activate ## Prepara o ambiente de desenvolvimento.
	@python3 -m pip install --upgrade pip

check: ## Verifica os estilos de código com isort, black, e flake8.
	@echo "$(BOLD)$(BLUE)Verificando estilos e formatos...$(RESET)"
	. $(VENV_DIR)
	@python3 -m isort --check --diff $(ISORT_ARGS) $(SRC_DIRS) || echo "$(RED)Checagem do isort falhou$(RESET)"
	@python3 -m black --check $(SRC_DIRS) || echo "$(RED)Checkagem do black falhou$(RESET)"
	@flake8 $(SRC_DIRS) || echo "$(RED)Checagem do flake8 falhou$(RESET)"

format: ## Formata o código usando isort e black.
	@echo "$(BOLD)$(BLUE)Formatando o código...$(RESET)"
	. $(VENV_DIR)
	@python3 -m isort --apply $(ISORT_ARGS) $(SRC_DIRS) || echo "$(RED)Formatação do isort falhou$(RESET)"
	@python3 -m black $(SRC_DIRS) || echo "$(RED)Formatação do black falhou$(RESET)"

run_spider: ## Roda um spider do Scrapy.
	@echo "$(BOLD)$(BLUE)Rodando Spider: $(SPIDER)...$(RESET)"
	. $(VENV_DIR)
	@cd $(SRC_DIRS) && scrapy crawl $(SPIDER)

sql: ## Inicia o shell interativo do SQLite3.
	@echo "$(BOLD)$(BLUE)Inicializando SQLite3 shell...$(RESET)"
	. $(VENV_DIR)
	@cd $(SRC_DIRS) && sqlite3 querido-diario.db

clean: ## Limpando os diretórios de dados.
	@echo "$(BOLD)$(BLUE)Limpando o diretório de dados...$(RESET)"
	. $(VENV_DIR)
	@find ./$(SRC_DIRS)/data/* -type d -exec rm -rv {} \;
	@echo "$(GREEN)Limpeza completa.$(RESET)"

shell: ## Inicia o shell interativo do Scrapy.
	@echo "$(BOLD)$(BLUE)Inicializando o shell interativo...$(RESET)"
	. $(VENV_DIR)
	@cd $(SRC_DIRS) && scrapy shell

run_spider_since: ## Roda um spider do Scrapy com data de início.
	@echo "$(BOLD)$(BLUE)Inicializando spider com data definida: $(START_DATE)...$(RESET)"
	. $(VENV_DIR)
	@cd $(SRC_DIRS) && scrapy crawl -a start_date=$(START_DATE) $(SPIDER)

compile: ## Compila os arquivos requirements.in e requirements-dev.in.
	@echo "$(BOLD)$(BLUE)Compilando requerimentos, por favor aguarde...$(RESET)"
	. $(VENV_DIR)
	@cd data_collection; \
	pip-compile --upgrade --no-annotate --allow-unsafe --generate-hashes requirements.in; \
	pip-compile --upgrade --no-annotate --allow-unsafe --generate-hashes requirements-dev.in

.venv/bin/activate: data_collection/requirements-dev.txt
	@echo "$(BOLD)$(BLUE)Preparando ambiente de desenvolvimento, por favor aguarde...$(RESET)"
	@python3 -m venv .venv
	@. $(VENV_DIR)
	pip install -r data_collection/requirements-dev.txt && pre-commit install || echo "$(RED)Erro ao instalar dependências.$(RESET)"
