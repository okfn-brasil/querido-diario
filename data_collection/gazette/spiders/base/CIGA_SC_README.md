# Spider Base CIGA/SC - Diário Oficial dos Municípios de Santa Catarina

Este documento explica a estrutura e o funcionamento do spider base para o sistema CIGA/SC (Consórcio de Inovação na Gestão Pública de Santa Catarina).

## 📋 Visão Geral

O sistema CIGA/SC (https://edicao.dom.sc.gov.br/) publica o Diário Oficial dos Municípios de Santa Catarina (DOM/SC). Este sistema consolida publicações oficiais de diversos municípios menores de Santa Catarina em um único portal.

### Características Principais

- **Edição Geral**: Um PDF consolidado contendo publicações de múltiplos municípios (~130 municípios/dia)
- **Fatiamento Automático**: O spider baixa 1 PDF grande e divide em N PDFs pequenos (1 por município)
- **Sumário**: As primeiras páginas listam todos os municípios que publicaram
- **Mapeamento IBGE**: 100% dos municípios são automaticamente mapeados para códigos IBGE
- **Estrutura**: Cada município tem uma seção no PDF com suas publicações
- **Formato Variável**: O sumário pode ter múltiplos municípios por linha (3 por linha, separados por pontos)

## 🏗️ Estrutura do PDF da Edição Geral

### Páginas 1-2: SUMÁRIO
Lista todos os municípios que publicaram naquela edição:
```
SUMÁRIO
MUNICÍPIOS
Água Doce .........................................3
Águas de Chapecó ..................................29
Alfredo Wagner ....................................32
...
```

### Páginas 3+: CONTEÚDO DAS PUBLICAÇÕES
Cada município tem uma seção começando com:
1. Nome do Município
2. "Prefeitura" ou "Câmara"  
3. Publicações oficiais (decretos, leis, editais, licitações, etc.)

**Exemplo:**
```
14/01/2026 (Quarta-feira) DOM/SC - Edição N° 5040 Página 3

Água Doce
Prefeitura

PROCESSO LICITATÓRIO Nº. 3/2026/PMAD
...
```

## 🕷️ Uso do Spider

### Spider Base: `BaseCigaSCSpider`

Localização: `gazette/spiders/base/ciga_sc.py`

**⚠️ USO RECOMENDADO: Edição Geral com Fatiamento Automático**

O spider foi projetado para processar a **Edição Geral** de forma eficiente:
- Baixa 1 PDF grande (1x download HTTP)
- Fatia automaticamente em ~120-130 PDFs pequenos
- Mapeia 100% dos municípios para códigos IBGE
- Gera 1 item Gazette por município

#### Edição Geral (Recomendado - Fatiamento Automático)

```python
from datetime import date
from gazette.spiders.base.ciga_sc import BaseCigaSCSpider

class ScEdicaoGeralSpider(BaseCigaSCSpider):
    name = "sc_edicao_geral"
    TERRITORY_ID = "4200000"  # Código do estado de SC
    municipality_id = "-1"  # -1 = Edição Geral (ativa fatiamento)
    start_date = date(2024, 1, 1)
```

**Executar:**
```bash
scrapy crawl sc_edicao_geral -a start=2026-01-14 -a end=2026-01-14
```

**Resultado:**
- 1 requisição HTTP
- ~131 items Gazette gerados
- ~131 PDFs salvos em `/tmp/ciga_sc_split/YYYY-MM-DD_EDICAO/`
- Formato: `{CODIGO_IBGE}_{DATA}_{EDICAO}.pdf`

#### Município Específico (Não Recomendado)

⚠️ **Nota:** A maioria dos municípios de SC publica na Edição Geral, não em edições separadas. Use esta opção apenas para municípios que têm edições próprias (ex: alguns municípios maiores podem ter edições separadas).

```python
from datetime import date
from gazette.spiders.base.ciga_sc import BaseCigaSCSpider

class ScMunicipioSpider(BaseCigaSCSpider):
    name = "sc_municipio"
    TERRITORY_ID = "4200000"  # Código IBGE do município
    municipality_id = "146"  # Código no sistema CIGA
    start_date = date(2024, 8, 5)
```

## 🔧 Extração de Informações dos Municípios

### Módulos Principais

#### 1. `gazette/utils/pdf_utils.py` - Processamento de PDF

Funções para extrair e fatiar PDFs da Edição Geral:

```python
from gazette.utils.pdf_utils import (
    extract_municipalities_from_pdf,
    split_pdf_by_municipalities
)

# Extrair lista de municípios do sumário
municipalities = extract_municipalities_from_pdf('edicao_5040.pdf')
# Resultado: {'Água Doce': 3, 'Águas de Chapecó': 29, ...}

# Fatiar PDF por município
results = split_pdf_by_municipalities(
    'edicao_5040.pdf',
    municipalities,
    temp_dir='/tmp/split',
    save_to_disk=True  # True para debug
)
# Retorna: [(nome, pag_inicio, pag_fim, pdf_bytes), ...]
```

#### 2. `gazette/utils/territory_mapping.py` - Mapeamento IBGE

Mapeia nomes de municípios para códigos IBGE:

```python
from gazette.utils.territory_mapping import (
    match_municipalities_from_summary,
    get_cached_sc_territories
)

# Mapear municípios para códigos IBGE
sc_territories = get_cached_sc_territories()
matched, not_found = match_municipalities_from_summary(
    ['Água Doce', 'Chapecó', 'São José'],
    sc_territories
)

# matched: {'Água Doce': '4200408', 'Chapecó': '4202404', ...}
# not_found: []  # Lista vazia = 100% de sucesso!
```

### Funções Disponíveis

#### `extract_municipalities_from_pdf(pdf_path)`
Extrai a lista de municípios e suas páginas do sumário do PDF.

**Parâmetros:**
- `pdf_path` (str): Caminho para o arquivo PDF

**Retorna:**
- `Dict[str, int]`: Dicionário {município: página_inicial}

#### `split_pdf_by_municipalities(pdf_path, municipalities_pages, temp_dir, save_to_disk)`
Fatia o PDF da Edição Geral em múltiplos PDFs (1 por município).

**Parâmetros:**
- `pdf_path` (str): Caminho do PDF completo
- `municipalities_pages` (Dict[str, int]): Dicionário {município: página}
- `temp_dir` (str, optional): Diretório para salvar PDFs
- `save_to_disk` (bool): Se True, salva em disco (debug mode)

**Retorna:**
- `List[Tuple[str, int, int, bytes]]`: Lista de (nome, pag_inicio, pag_fim, pdf_bytes)

#### `match_municipalities_from_summary(municipalities, sc_territories)`
Mapeia lista de municípios para códigos IBGE.

**Parâmetros:**
- `municipalities` (List[str]): Lista de nomes de municípios
- `sc_territories` (Dict): Dicionário de territórios de SC

**Retorna:**
- `Tuple[Dict[str, str], List[str]]`: (mapeados, não_encontrados)

## 📊 Análise de PDF

Um script de análise está disponível para entender a estrutura:

```bash
cd gazette/spiders/base
python analyze_pdf.py
```

Este script:
- Extrai o sumário completo
- Lista todos os municípios que publicaram
- Mostra a página inicial de cada município
- Verifica a estrutura das páginas de conteúdo

## 🔄 Fluxo de Trabalho

### Fluxo Completo do Spider (Edição Geral com Fatiamento)

1. **Busca**: Spider acessa `https://edicao.dom.sc.gov.br/`
2. **Filtragem**: Aplica filtros de data (`start_date` e `end_date`)
3. **Identificação**: Encontra Edição Geral do dia X
4. **Download**: Baixa o PDF completo (1x requisição HTTP, ~40 MB)
5. **Extração**: Processa PDF e extrai sumário das primeiras páginas
6. **Mapeamento**: Identifica ~120-130 municípios e mapeia para códigos IBGE (100% de sucesso)
7. **Fatiamento**: Divide o PDF em N arquivos (1 por município)
8. **Salvamento**: Gera PDFs individuais em `/tmp/ciga_sc_split/DATA_EDICAO/`
9. **Yield**: Cria N items Gazette (1 por município) com `file://` URLs
10. **Pipeline**: Pipeline do Scrapy processa e envia para S3

### Detalhes Técnicos

**Processamento do PDF:**
```
PDF Original: edicao_5040_assinada.pdf (39 MB, 1.310 páginas)
    ↓Real - Edição N° 5040 (14/01/2026)

### Dados da Edição Original
- **Total de páginas:** 1.310
- **Municípios que publicaram:** 124
- **Arquivo:** `1768412435_edicao_5040_assinada.pdf`
- **Tamanho:** 39,42 MB
- **Data de publicação:** 14/01/2026 (Quarta-feira)

### Resultado do Processamento

**Estatísticas:**
- ✅ 131 municípios identificados no sumário
- ✅ 131 municípios mapeados para IBGE (100% de sucesso)
- ✅ 131 PDFs gerados (~122 MB total)
- ✅ Tempo de processamento: ~2 minutos
- ✅ 0 erros de mapeamento

**Nota Importante sobre Regex:** O sumário do PDF pode ter municípios sem espaço antes dos pontos (ex: `"Faxinal dos Guedes.....473"` vs `"Água Doce .....3"`). O regex foi ajustado para capturar ambos os formatos com `\s*\.{2,}` (zero ou mais espaços, seguidos de 2+ pontos).

**Exemplos de Municípios Processados:**

| Município | Código IBGE | Páginas | Tamanho | Arquivo Gerado |
|-----------|-------------|---------|---------|----------------|
| Água Doce | 4200408 | 3-28 (26) | 593 KB | `4200408_2026-01-14_5040.pdf` |
| Águas de Chapecó | 4200507 | 29-31 (3) | 177 KB | `4200507_2026-01-14_5040.pdf` |
| Alfredo Wagner | 4200705 | 32-40 (9) | 717 KB | `4200705_2026-01-14_5040.pdf` |
| Blumenau | 4202404 | 103-131 (29) | 856 KB | `4202404_2026-01-14_5040.pdf` |
| Chapecó | 4204202 | 288-290 (3) | 638 KB | `4204202_2026-01-14_5040.pdf` |
| Lages | 4209300 | 600-602 (3) | 458 KB | `4209300_2026-01-14_5040.pdf` |
| São José | 4216602 | 1059-1061 (3) | 345 KB | `4216602_2026-01-14_5040.pdf` |
| Xaxim | 4219705 | 1256-1310 (55) | 1.1 MB | `4219705_2026-01-14_5040.pdf` |

**Diretório de Saída:**
```
/tmp/ciga_sc_split/2026-01-14_5040/
├── 4200408_2026-01-14_5040.pdf  (Água Doce - 26 págs)
├── 4200507_2026-01-14_5040.pdf  (Águas de Chapecó - 3 págs)
├── 4200705_2026-01-14_5040.pdf  (Alfredo Wagner - 9 págs)
├── 4205209_2026-01-14_5040.pdf  (Erval Velho - 71 págs)
├── 4205308_2026-01-14_5040.pdf  (Faxinal dos Guedes - 1 pág)
├── 4205704_2026-01-14_5040.pdf  (Garopaba - 1 pág)
├── ...
└── 4219705_2026-01-14_5040.pdf  (Xaxim - 55 págs)
``` - 14/01/2026**
- **Total de páginas:** 1.310
- **Municípios que publicaram:** 124
- **Arquivo:** `1768412435_edicao_5040_assinada.pdf`
- **Tamanho:** 39,42 MB

**Alguns municípios desta edição:**
- Água Doce (página 3)
- Águas de Chapecó (página 29)
- Alfredo Wagner (página 32)
- Blumenau (página 103)
- Chapecó (página 288)
- Lages (página 600)
- ... 119 outros

## 🎯 Casos de Uso

### 1. Coletar todos os municípios de SC de um período (Recomendado)
```bash
# Coleta edições gerais e fatia automaticamente30 municípios/dia):
# - 20 requisições HTTP (1 PDF por dia)
# - ~2.600 items Gazette gerados (20 dias × 130 municípios)
# - ~2.600 PDFs individuais salvos
```

### 2. Coletar apenas uma data específica para teste
```bash
scrapy crawl sc_edicao_geral -a start=2026-01-14 -a end=2026-01-14

# Resultado:
# - 1 requisição HTTP
# - ~131 items Gazette
# - ~131ado:
# - 1 requisição HTTP
# - ~124 items Gazette
# - ~124 PDFs em /tmp/ciga_sc_split/2026-01-14_EDICAO/
```

### 3. Verificar quais municípios publicaram (análise offline)
```python
from gazette.utils.pdf_utils import extract_municipalities_from_pdf
from gazette.utils.territory_mapping import match_municipalities_from_summary

# Após baixar o PDF
municipalities = extract_municipalities_from_pdf('edicao_5040.pdf')
print(f"Municípios que publicaram: {len(municipalities)}")

# Mapear para códigos IBGE
matched, not_found = match_municipalities_from_summary(
    list(municipalities.keys())
)
print(f"Mapeados com sucesso: {len(matched)}")
print(f"Não encontrados: {len(not_found)}")

# Listar todos
for name in sorted(municipalities.keys()):
    ibge_code = matched.get(name, 'N/A')
    page = municipalities[name]
    print(f"{ibge_code} - {name:40s} (página {page})")
```

### 4. Processar PDF já baixado (script standalone)
```python
# Ver: gazette/spiders/base/test_split_pdf.py
cd /home/grisolfi/Dev/querido-diario/data_collection
PYTHONPATH=. python gazette/spiders/base/test_split_pdf.py
```

## 📦 Dependências

Dependências principais (já incluídas em `requirements.in`):

- `scrapy` - Framework de web scraping
- `pdfplumber` - **Obrigatório** - Extração de texto e sumário de PDFs
- `pypdf` - **Obrigatório** - Manipulação e fatiamento de PDFs

**Instalação:**
```bash
cd data_collection
pip install -r requirements.txt
. Já tem spiders específicos: `sc_florianopolis_2009` e `sc_florianopolis_2024`

2. **Edição Geral é a Fonte Principal**: 
   - ~130 municípios menores de SC publicam na Edição Geral
   - 1 PDF consolidado por dia útil
   - Processamento único com fatiamento automático

3. **Mapeamento IBGE 100% Eficaz**:
   - Todos os 295 municípios de SC estão mapeados
   - Normalização automática de nomes (acentos, preposições)
   - Taxa de sucesso observada: 131/131 = 100%

4. **Sumário com Formato Variável**:
   - Múltiplos municípios por linha (geralmente 3)
   - Espaçamento inconsistente: `"Água Doce .....3"` vs `"Faxinal dos Guedes.....473"`
   - Regex robusto: `\s*\.{2,}` captura ambos os formatos

4. **Modo Debug Ativo**:
   - PDFs são salvos em `/tmp/ciga_sc_split/` para inspeção
   - Útil pa31 arquivos (~122 MB total)
   - Uso de memória: ~150-200 MB durante processamento

6. **Variação no Número de Municípios**:
   - O número de municípios varia por dia (não fixo em 131)
   - Depende das atividades de publicação de cada município
   - Já observado: 120-135200 MB durante processamento

6. **Variação no Número de Municípios**:
   - O número de municípios varia por dia (não fixo em 124)
   - Depende das atividades de publicação de cada município
   - Já observado: 100-130 municípios por edição
**Verificar instalação:**
```bash
python -c "import pdfplumber, pypdf; print('✓ Dependências OK')"
```

## ⚠️ Observações Importantes

1. **Florianópolis**: Possui seu próprio diário oficial, não usa o DOM/SC
2. **Municípios Maiores**: Alguns municípios podem ter edições separadas
3. **Edição Geral**: Consolida principalmente municípios menores
4. **Paginação**: O site usa paginação, o spider navega automaticamente
5. **PDFs Grandes**: Edições gerais podem ter mais de 1.000 páginas
6. **Filtro de datas é client-side**: o portal ignora `dt_edicao_de/dt_edicao_ate`; o spider pagina em ordem descendente e filtra localmente, parando ao atingir datas anteriores a `start_date`.

## 📂 Saída de PDFs fatiados

- Os PDFs gerados são salvos em `/tmp/ciga_sc_split/<DATA>_<EDICAO>/` (1 arquivo por município, nome: `{IBGE}_{DATA}_{EDICAO}.pdf`).
- Para compartilhar, compacte a pasta do dia: `cd /tmp/ciga_sc_split && tar -czf <DATA>_<EDICAO>.tar.gz <DATA>_<EDICAO>` (ex.: `2025-03-18_4789.tar.gz`).

## 🔮 Funcionalidades Futuras

- [x] ✅ Dividir PDF da Edição Geral por município - **IMPLEMENTADO**
- [x] ✅ Mapeamento automático para códigos IBGE - **IMPLEMENTADO**
- [x] ✅ Fatiamento automático de PDFs - **IMPLEMENTADO**
- [ ] Cache de sumários já processados (para reprocessamento)
- [ ] Modo produção sem salvar PDFs em disco
- [ ] Extração de metadados específicos por tipo de publicação
- [ ] Indexação de publicações por tipo (licitação, decreto, portaria, etc.)
- [ ] Detecção de edições extras automaticamente
- [ ] Estatísticas de publicações por município
- [ ] Histórico de frequência de publicações

## 📚 Referências

- **Portal DOM/SC**: https://diariomunicipal.sc.gov.br/
- **Edições Anteriores**: https://edicao.dom.sc.gov.br/?r=site/edicoes
- **CIGA**: https://consorciociga.gov.br/
- **Documentação Querido Diário**: https://github.com/okfn-brasil/querido-diario

## 📊 Estatísticas de Implementação

### Teste Real - Edição N° 5040 (14/01/2026)

```
Input:  1 PDF  (39,4 MB, 1.310 páginas)
Output: 131 PDFs (~122 MB, média 930 KB/município)

Processamento:
├── Extração do sumário: ~5 segundos
├── Mapeamento IBGE: <1 segundo  (100% de sucesso)
├── Fatiamento do PDF: ~2 minutos
└── Total: ~2min 10seg

Taxa de Sucesso:
├── Municípios identificados: 131/131 (100%)
├── Mapeamento IBGE: 131/131 (100%)
├── PDFs gerados: 131/131 (100%)
└── Items Gazette: 131/131 (100%)

Eficiência:
├── 1 requisição HTTP (vs 131 requisições sem fatiamento)
├── Processamento único do PDF
└── Redução de ~99% no tráfego de rede para coletas subsequentes

Correção de Bug (15/01/2026):
├── Problema: Municípios como "Faxinal dos Guedes" não eram capturados
├── Causa: Sumário sem espaço antes dos pontos ("Faxinal dos Guedes.....473")
├── Solução: Regex ajustado de `\s+\.+` para `\s*\.{2,}`
└── Resultado: +7 municípios encontrados (124 → 131)
```

---

**Status**: ✅ Implementação completa e testada
**Data**: Janeiro 2026
**Versão**: 1.0.0
