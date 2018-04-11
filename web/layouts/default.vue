<template>
  <div>
    <navbar/>

    <section class="hero is-medium is-gapless hero-main-section">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-5">
              <img src="/hero_logo.png" alt="Operação Serenata de Amor" class="hero-logo">
            </div>
          </div>
          <h1 class="title">Diários Oficiais</h1>
        </div>
      </div>
    </section>

    <nuxt/>
  </div>
</template>

<style>
body {
  font-family: 'Anonymous Pro', monospace;
  font-size: 28px;
}

h1,
h2 {
  font-weight: 600;
  text-transform: uppercase;
}

p {
  margin-bottom: 30px;
}

.hero-main-section {
  background-image: url(/static/bg.gif);
  background-size: cover;
}

.hero .title {
  color: #fff;
  font-size: 4rem;
}
</style>

<script>
import Navbar from '~/components/Navbar.vue'

export default {
  components: {
    Navbar,
  }
}
</script>
