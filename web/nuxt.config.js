module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'Diário Oficial | Operação Serenata de Amor',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Diários Oficiais acessíveis a todos.' },
      { property: 'og:url', content: 'https://diario.serenata.ai/' },
      { property: 'og:type', content: 'website' },
      { property: 'og:title', content: 'Diário Oficial | Operação Serenata de Amor' },
      { property: 'og:description', content: 'https://diario.serenata.ai/' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Anonymous+Pro' },
    ]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  },
  css: [
    'bulma',
  ],
}
