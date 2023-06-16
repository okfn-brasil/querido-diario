**AO ABRIR** um Pull Request de um novo raspador (spider), marque com um `X` cada um dos items do checklist 
abaixo. **NÃO ABRA** um novo Pull Request antes de completar todos os items obrigatorios abaixo.

#### Checklist - Novo spider - Obrigatorio
- [ ] Você executou uma extração completa do spider localmente e os dados retornados estavam corretos.
- [ ] Você executou uma extração por período (`start_date` e `end_date` definidos) ao menos uma vez e os dados retornados estavam corretos.
- [ ] Você verificou que não existe nenhum erro nos logs (`log_count/ERROR` igual a zero).
- [ ] Você definiu o atributo de classe `start_date` no seu spider com a data do Diário Oficial mais antigo disponível na página da cidade.
- [ ] Você garantiu que todos os campos que poderiam ser extraídos foram extraídos [de acordo com a documentação](https://docs.queridodiario.ok.org.br/pt/latest/escrevendo-um-novo-spider.html#definicao-de-campos).

### Opcional Check

- [ ] Demora mais de uma hora para fazer a coleta de todos os diarios.
- [ ] Tem mais de um site que fornece os diarios.
- [ ] Mais de 10 anos estão disponiveis para coletar.
- [ ] PDFs vem com a extenção correta.
- [ ] Ultilizo de algum "class" predefinido.
- [ ] Ouve algum bloqueio de IP ou alguma interropição de conexão durante alguma coleta.

#### Descrição

<Descreva o seu Pull Request informando a issue (caso exista) que está sendo solucionada ou uma descrição do código apresentado>
