<template>
  <div>
    <navbar/>

    <section class="hero is-medium is-gapless hero-main-section">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-5">
              <img src="~/assets/hero_logo.png" alt="Operação Serenata de Amor" class="hero-logo">
            </div>
          </div>
          <h1 class="title">Diário Oficial</h1>
        </div>
      </div>
    </section>

    <nuxt/>

    <footer class="footer">
      <div class="container">
        <div class="columns">
          <div class="column is-one-third">
            <ul>
              <li><a href="https://twitter.com/RosieDaSerenata">No Twitter</a></li>
              <li><a href="https://www.facebook.com/operacaoSerenataDeAmor">No Facebook</a></li>
              <li><a href="https://github.com/okfn-brasil/diario-oficial">No GitHub</a></li>
              <li><a href="mailto:contato@serenata.ai">Contato</a></li>
            </ul>
          </div>
          <div class="column is-one-third">
            <a href="https://br.okfn.org/"><img src="~/assets/okbr.png" alt="Open Knowledge Brasil"></a>
          </div>
        </div>
      </div>
    </footer>

    <modal/>
  </div>
</template>

<style>
body {
  font-family: "Anonymous Pro", monospace;
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

a {
  text-decoration: underline;
}

a:hover {
  color: #43007f;
}

a.navbar-item:hover,
a.navbar-item.is-active,
a.navbar-link:hover,
a.navbar-link.is-active {
  color: #43007f;
}


.hero-main-section {
  background-color: #000;
  background-image: url('~/assets/bg.gif');
  background-size: cover;
  color: #fff;
}

.hero .title {
  color: #fff;
  font-size: 4rem;
}

.footer {
  background-color: #43007f;
  color: #fff;
  text-transform: uppercase;
}

.footer a {
  color: #fff;
}

.footer a:hover {
  color: #E6E6E6;
}
</style>

<script>
import Modal from "~/components/Modal.vue"
import Navbar from "~/components/Navbar.vue"

export default {
  components: {
    Modal,
    Navbar,
  }
};
</script>
