<template>
  <div>
    <div class="section">
      <div class="container">
        <p><strong>Para evitar que a administração pública pague preços acima do valor</strong> de mercado, todo órgão público deve seguir a Lei de Licitações. Nela, é previsto a abertura de concorrência de preços: o órgão diz o que precisa e empresas competem pelo preço mais barato.</p>
        <p>Mas a mesma lei também prevê excessões: <strong>compras inferiores a R$ 8 mil</strong>, por exemplo, dispensam esse processo de concorrência pelo menor preço. Essa dispensa de licitação deve ser divulgada na publicação oficial do órgão: o Diário Oficial.</p>
        <p>Hoje, Diários são publicados oficialmente em PDF, <strong>um formato pouco convidativo para ser auditado</strong>.</p>
        <p><strong>Queremos mudar isso.</strong></p>
      </div>
    </div>

    <div class="section">
      <div class="container">
        <h2>Municípios atendidos</h2>
        <p>
          <ul>
            <li>RS - Porto Alegre</li>
          </ul>
        </p>
      </div>
    </div>

    <div class="section">
      <div class="container">
        <h2>Todas dispensas de licitação desde 2015</h2>

        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th><abbr title="Data de publicação oficial">Data</abbr></th>
              <th><abbr title="Órgão responsável pela compra">Órgão</abbr></th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <th><abbr title="Data de publicação oficial">Data</abbr></th>
              <th><abbr title="Órgão responsável pela compra">Órgão</abbr></th>
            </tr>
          </tfoot>
          <tbody>
            <tr v-for="item in biddingExemptions" :key="item.id">
              <td>{{ item.gazette.date }}</td>
              <td v-if="item.gazette.power == 'executive'">Prefeitura de Porto Alegre</td>
              <td v-else-if="item.gazette.power == 'legislature'">Câmara Municipal de Porto Alegre</td>
              <td>
                <button type="button" class="button is-info">
                  Mais informações
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- <div class="modal">
      <div class="modal-background"></div>
      <div class="modal-content">
        <p>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Odio aliquam similique obcaecati ipsam soluta iusto commodi veniam delectus explicabo rerum fugiat, iste beatae exercitationem mollitia, non eaque sit minima temporibus.
        </p>
      </div>
      <button class="modal-close is-large" aria-label="close"></button>
    </div> -->
  </div>
</template>

<style>

</style>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['biddingExemptions']),
  },
  async fetch ({ store, params }) {
    let results = await axios.get('http://api:3000/bidding_exemptions?select=*,gazette{date,is_extra_edition,file_url}')
    store.commit('updateBiddingExemptions', results)
  }
}
</script>
