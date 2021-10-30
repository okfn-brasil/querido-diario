# Contribuindo

______________________________________

_[Click here](languages/en-US/CONTRIBUTING.md) to read this article in english._
______________________________________


*Este projeto foi lançado com um [Código de Conduta de Contribuição](CODE_OF_CONDUCT.md). Ao participar dele, você concorda em cumprir seus termos.*

Uma vez que o Diário Oficial se propõe a ser uma fonte confiável de publicações oficiais do governo, todas as fontes de dados também devem ser confiáveis. Uma empresa privada que publica diários do governo sem permissão oficial, por exemplo, não é uma fonte confiável.

No momento, o projeto visa os 100 municípios brasileiros com maior população, coletando todos os diários desde 2015. Se você quiser nos ajudar a atingir essa meta, estamos acompanhando o andamento dos raspadores no arquivo [CITIES.md](CITIES.md). Dê uma olhada nele se quiser saber em que cidades outras pessoas colaboradoras já estão trabalhando.

## Começando a contribuir

Se você nunca contribuiu com nenhum projeto de código aberto, existem tarefas pensadas especialmente para você. Elas são [rotuladas como "bom primeiro problema" (_good first issue_)](https://github.com/okfn-brasil/diario-oficial/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Antes de começar, deixe um comentário dizendo que você planeja trabalhar nisso e aproveite para tirar dúvidas, se houver.

Às vezes, a comunidade organiza eventos para resolver vários problemas em um curto espaço de tempo. Especialmente nesses casos, um problema (_issue_) ou _pull request_ pode ser considerado abandonado quando está esperando ação da pessoa contribuidora e não recebe atualizações por algumas semanas. Avise-nos se você precisar de mais tempo, para que não acabemos encerrando por engano a contribuição já iniciada.


### Configurar

Por favor, consulte o [arquivo README](README.md) para saber como configurar o projeto. Além disso, leia o `Makefile` para entender as tarefas disponíveis e o que elas executam.


### Escrevendo raspadores para novos municípios

Para coletar os diários dos sites oficiais, usamos uma estrutura de raspagem chamada [Scrapy](https://docs.scrapy.org). Você pode acessar seu [tutorial oficial](https://docs.scrapy.org/en/latest/intro/tutorial.html), muito útil para se familiarizar com sua arquitetura. Nosso projeto pode ser encontrado na pasta [`data_collection`](data_collection).

Dois comandos podem ser especialmente úteis: `scrapy shell` and `scrapy crawl`.

O Scrapy tem uma interface de shell para experimentar raspadores ou spiders (como preferir chamá-los). Para ver como o Scrapy lê uma página da web antes de escrever um spider para isso, tente o seguinte, substituindo a URL pelo site de um município diferente:

```console
$ scrapy shell http://www2.portoalegre.rs.gov.br/dopa/
```

Para executar um spider existente, consulte o [arquivo README](README.md).

## Formatação automatizada do código 

O projeto usa [Black](https://github.com/psf/black) como uma ferramenta para formatar e verificar de forma automatizada o estilo do código e [isort](https://github.com/pycqa/isort) para ordenar as importações. A integração contínua (CI) vai **falhar** se seu código não estiver formatado corretamente de acordo com essas ferramentas.

Se você seguiu as instruções de configuração, instalando ganchos de pré-commit, é possível que você nunca precise executar essas ferramentas manualmente, pois elas serão executadas antes de cada _commit_. Porém, se você quiser executá-las em todos os arquivos do projeto, você pode usar o comando `make format`, que roda essas ferramentas.

## Diretrizes para pessoas mantenedoras

Esta seção é um espaço para os mantenedores do projeto. Uma vez que a revisão do código e a organização do repositório fazem parte do processo de contribuição, todas as diretrizes de revisão do código são de interesse público para todas as pessoas na comunidade.

### Responsabilidades da pessoa mantenedora do Querido Diário:

- Respeite o [código de conduta](https://github.com/okfn-brasil/querido-diario/blob/main/CODE_OF_CONDUCT.md) e garanta que quem pode ter sofrido assédio tenha um canal de apoio.
- Justifique sempre uma sugestão de acordo com as práticas já adotadas no projeto - legibilidade e simplicidade. É essencial para um projeto cívico ter uma estrutura o mais fácil possível para iniciantes.
- As pessoas mantenedoras devem **rodar todos os spiders antes de fundi-los ao projeto (_merge_)**.
- Se um _Pull Request_ tiver muitos commits e suas mensagens não forem claras, use a opção *squash and merge*. Não é necessário fazer squash quando as práticas de commits forem boas. Veja um exemplo: [Pull Request](https://github.com/okfn-brasil/querido-diario/pull/252/commits).