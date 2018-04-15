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
        <h2 id="bidding-exemptions">Todas dispensas de licitação desde 2015</h2>

        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th><abbr title="Data de publicação oficial">Data</abbr></th>
              <th>Município</th>
              <th>Valor</th>
              <th>Descrição</th>
              <th></th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <th><abbr title="Data de publicação oficial">Data</abbr></th>
              <th>Município</th>
              <th>Valor</th>
              <th>Descrição</th>
              <th></th>
            </tr>
          </tfoot>
          <tbody>
            <tr v-for="item in biddingExemptions" :key="item.id">
              <td>{{ new Date(item.date).toLocaleDateString('pt-BR') }}</td>
              <td>Porto Alegre</td>
              <td v-if="item.value">{{ formatCurrency(item.value) }}</td>
              <td v-else></td>
              <td v-if="item.object && item.object.length > 200" :title="item.object">{{ truncate(item.object, 200) }}</td>
              <td v-else>{{ item.object }}</td>
              <td>
                <button type="button" class="button is-info" @click="openModal(item)">
                  Detalhes
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style>
.button.is-info {
  background-color: #43007f;
}

.button.is-info:hover {
  background-color: #E6E6E6;
  color: #43007f;
}
</style>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

const BIDDING_EXEMPTIONS_API_URL = process.env.API_URL +
  '/bidding_exemptions' +
  '?select=*,gazette{file_url,is_extra_edition,power}' +
  '&order=date.desc'

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

export default {
  computed: {
    ...mapState(['biddingExemptions']),
  },
  methods: {
    formatCurrency (number) {
      return currencyFormatter.format(number)
    },
    openModal: function(biddingExemption) {
      this.$store.commit('openModal', biddingExemption)
    },
    truncate (string, length) {
       if (string && string.length > length)
          return string.substring(0, length) + '…'
       else
          return string
    },
  },
  async fetch ({ store, params }) {
    let results = await axios.get(BIDDING_EXEMPTIONS_API_URL)
    store.commit('updateBiddingExemptions', results)
  }
}
</script>
