<template>
  <div class="modal" v-bind:class="{ 'is-active': isModalActive }">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Dispensa de licitação</p>
        <button class="delete" aria-label="close" @click="closeModal"></button>
      </header>
      <section class="modal-card-body">
        <div class="content">
          <dl>
            <span v-for="(item, key) in biddingExemption.data" :key="item.id">
              <dt>{{ key }}</dt>
              <dd>{{ item }}</dd>
            </span>
            <dt>TEXTO ORIGINAL</dt>
            <dd>{{ biddingExemption.source_text }}</dd>
          </dl>
        </div>
      </section>
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

export default {
  computed: {
    ...mapState(['biddingExemption', 'isModalActive']),
  },
  methods: {
    closeModal: function() {
      this.$store.commit('closeModal')
    }
  },
}
</script>
