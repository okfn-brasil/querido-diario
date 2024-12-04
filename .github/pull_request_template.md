**AO ABRIR** uma *Pull Request* de um novo raspador (*spider*), marque com um `X` cada um dos items da checklist abaixo. Caso algum item não seja marcado, JUSTIFIQUE o motivo.

#### Layout do site publicador de diários oficiais
Marque apenas um dos itens a seguir:
- [ ] O *layout* não se parece com nenhum caso [da lista de *layouts* padrão](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/lista-sistemas-replicaveis.html)
- [ ] É um *layout* padrão e esta PR adiciona a spider base do padrão ao projeto junto com alguns municípios que fazem parte do padrão.
- [ ] É um *layout* padrão e todos os municípios adicionados usam a [classe de spider base](https://github.com/okfn-brasil/querido-diario/tree/main/data_collection/gazette/spiders/base) adequada para o padrão.

#### Código da(s) spider(s)
- [ ] O(s) raspador(es) adicionado(s) tem os [atributos de classe exigidos](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#UFMunicipioSpider).
- [ ] O(s) raspador(es) adicionado(s) cria(m) objetos do tipo Gazette coletando todos [os metadados necessários](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#Gazette).
- [ ] O atributo de classe [start_date](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#UFMunicipioSpider.start_date) foi preenchido com a data da edição de diário oficial mais antiga disponível no site.
- [ ] Explicitar o atributo de classe [end_date](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#UFMunicipioSpider.end_date) não se fez necessário.
- [ ] Não utilizo `custom_settings` em meu raspador.

#### Testes
- [ ] Uma coleta-teste **da última edição** foi feita. O arquivo de `.log` deste teste está anexado na PR.
- [ ] Uma coleta-teste **por intervalo arbitrário** foi feita. Os arquivos de `.log`e `.csv` deste teste estão anexados na PR.
- [ ] Uma coleta-teste **completa** foi feita. Os arquivos de `.log` e `.csv` deste teste estão anexados na PR.

#### Verificações
- [ ] Eu experimentei abrir alguns arquivos de diários oficiais coletados pelo meu raspador e verifiquei eles [conforme a documentação](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#diarios-oficiais-data-collection-data) não encontrando problemas.
- [ ] Eu verifiquei os arquivos `.csv` gerados pela minha coleta [conforme a documentação](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#tabela-da-coleta-arquivo-csv) não encontrando problemas.
- [ ] Eu verifiquei os arquivos de `.log` gerados pela minha coleta [conforme a documentação](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/raspadores.html#log-arquivo-log) não encontrando problemas.

#### Descrição

<Descreva o seu Pull Request informando a issue (caso exista) que está sendo solucionada ou uma descrição do código apresentado>
