<template>
  <div class="modal" v-if="isModalActive" :class="{ 'is-active': isModalActive }">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Dispensa de licitação</p>
        <button class="delete" aria-label="close" @click="closeModal"></button>
      </header>
      <section class="modal-card-body">
        <div class="content">
          <dl>
            <dt>DATA DE PUBLICAÇÃO</dt>
            <dd>{{ new Date(biddingExemption.date).toLocaleDateString('pt-BR') }}</dd>
            <dt>ÓRGÃO</dt>
            <dd v-if="biddingExemption.gazette.power == 'executive'">
              Prefeitura -
              {{ biddingExemption.gazette.territory.name }} ({{ biddingExemption.gazette.territory.state_code }})
            </dd>
            <dd v-else-if="biddingExemption.gazette.power == 'legislature'">
              Câmara Municipal -
              {{ biddingExemption.gazette.territory.name }} ({{ biddingExemption.gazette.territory.state_code }})
            </dd>
            <dd v-else-if="biddingExemption.gazette.power == 'executive_legislature'">
              Prefeitura e Câmara Municipal -
              {{ biddingExemption.gazette.territory.name }} ({{ biddingExemption.gazette.territory.state_code }})
            </dd>
            <dt>VALOR</dt>
            <dd v-if="biddingExemption.value">{{ formatCurrency(biddingExemption.value) }}</dd>
            <dd v-else><span class="tag is-warning">Não identificado automaticamente</span></dd>
            <dt>DESCRIÇÃO</dt>
            <dd v-if="biddingExemption.object">{{ biddingExemption.object }}</dd>
            <dd v-else><span class="tag is-warning">Não identificado automaticamente</span></dd>
            <dt>CONTRATADO</dt>
            <dd v-if="biddingExemption.contracted">{{ biddingExemption.contracted }}</dd>
            <dd v-else><span class="tag is-warning">Não identificado automaticamente</span></dd>
            <dt>CNPJ</dt>
            <dd v-if="biddingExemption.contracted_code">{{ biddingExemption.contracted_code.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5") }}</dd>
            <dd v-else><span class="tag is-warning">Não identificado automaticamente</span></dd>
            <hr>
            <strong>Diário Oficial</strong>
            <dt>TEXTO ORIGINAL</dt>
            <dd>{{ biddingExemption.source_text }}</dd>
          </dl>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a :href="biddingExemption.gazette.file_url" class="button" target="_blank">Diário Oficial</a>
      </footer>
    </div>
  </div>
</template>

<style>
.modal-card-title {
  margin-bottom: 0;
}

dt {
  font-weight: bold;
}

.content dd {
    margin-left: 0;
}
</style>

<script>
import { mapState } from 'vuex'

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

export default {
  computed: {
    ...mapState(['biddingExemption', 'isModalActive']),
  },
  methods: {
    closeModal: function() {
      this.$store.commit('closeModal')
    },
    formatCurrency (number) {
      return currencyFormatter.format(number)
    },
  },
}
</script>
