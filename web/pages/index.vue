<template>
  <div>
    <div class="section">
      <div class="container">
        <p><strong>Para evitar que a administração pública pague preços acima do valor</strong> de mercado, todo órgão público deve seguir a Lei de Licitações. Nela, é previsto a abertura de concorrência de preços: o órgão diz o que precisa e empresas competem pelo preço mais barato.</p>
        <p>Mas a mesma lei também prevê exceções: <strong>compras inferiores a R$ 8 mil</strong>, por exemplo, dispensam esse processo de concorrência pelo menor preço. Essa dispensa de licitação deve ser divulgada na publicação oficial do órgão: o Diário Oficial.</p>
        <p>Hoje, Diários são publicados oficialmente em PDF, <strong>um formato pouco convidativo para ser auditado</strong>.</p>
        <p><strong>Queremos mudar isso.</strong></p>
      </div>
    </div>

    <div class="section">
      <div class="container">
        <h2>Municípios atendidos</h2>

        <p>
          Nossa meta é começar pelos <strong>100 maiores municípios</strong> do Brasil. De acordo com o <abbr title="Instituto Brasileiro de Geografia e Estatística">IBGE</abbr>, eles representam mais de <strong>40% da população</strong> brasileira.
        </p>
        <p>
          Neste momento, temos 1 município e 7 outros em fase de finalização.
        </p>

        <ul class="municipalities-list">
          <li>RS - Porto Alegre</li>
        </ul>

        <div class="has-text-centered">
          <img src="~/assets/gem.gif" alt="" title="RS - Porto Alegre" class="municipality-icon municipality-active" />
          <img src="~/assets/gem.gif" alt="" title="" class="municipality-icon municipality-wip" v-for="y in 7" :key="y" />
          <img src="~/assets/gem.png" alt="" title="" class="municipality-icon" v-for="y in 2" :key="y" />
        </div>
        <div v-for="x in 9" :key="x" class="has-text-centered">
          <img src="~/assets/gem.png" alt="" title="" class="municipality-icon" v-for="y in 10" :key="y" />
        </div>
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
            <tr v-once v-for="item in biddingExemptions" :key="item.id">
              <td>{{ new Date(item.date).toLocaleDateString('pt-BR') }}</td>
              <td>{{ item.gazette.territory.name }} ({{ item.gazette.territory.state_code }})</td>
              <td v-if="item.value">{{ formatCurrency(item.value) }}</td>
              <td v-else><span class="tag is-warning">Não identificado automaticamente</span></td>
              <td v-if="item.object && item.object.length > 200" :title="item.object">{{ truncate(item.object, 200) }}</td>
              <td v-else-if="item.object">{{ item.object }}</td>
              <td v-else><span class="tag is-warning">Não identificado automaticamente</span></td>
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

.municipality-icon {
  filter: grayscale(1) contrast(50%);
  height: 45px;
  margin: -3px 10px;
  width: 45px;
}

.municipality-wip {
  filter: contrast(50%);
}

.municipality-active {
  filter: grayscale(0) contrast(100%);
}

.municipality-icon:first-child {
  margin-left: 0;
}

.municipality-icon:last-child {
  margin-right: 0;
}

.municipalities-list {
  margin-bottom: 30px;
}
</style>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

const BIDDING_EXEMPTIONS_API_URL = process.env.API_URL +
  '/bidding_exemptions' +
  '?select=*,gazette{file_url,is_extra_edition,territory_id,power,territory{name,state_code}}' +
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
