<template>
  <div>
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <nuxt-link to="/" class="navbar-item">
            <img src="/logo.png" alt="Operação Serenata de Amor" class="navbar-logo">
          </nuxt-link>

          <a role="button" class="navbar-burger" v-bind:class="{ 'is-active': isActive }" aria-label="menu" aria-expanded="false" @click="togglMenu">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>
        <div class="navbar-menu" v-bind:class="{ 'is-active': isActive }">
          <div class="navbar-end">
            <a class="navbar-item">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </nav>

    <div class="notification is-danger has-text-centered">
      <a href="https://apoia.se/serenata">Apoie o projeto</a>
    </div>
  </div>
</template>

<style>
.notification {
  text-transform: uppercase;
}

.navbar-logo {
  max-height: 50px;
}

.navbar-item {
  text-transform: uppercase;
}
</style>

<script>
export default {
  head: {
    htmlAttrs: {
      class: 'has-navbar-fixed-top',
    },
  },
  data: () => {
    return {
      isActive: false,
    }
  },
  methods: {
    togglMenu: function() {
      this.$data.isActive = !this.$data.isActive
    }
  }
}
</script>
