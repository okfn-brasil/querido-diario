import Vuex from 'vuex'

const createStore = () => {
  return new Vuex.Store({
    state: {
      biddingExemption: {},
      biddingExemptions: [],
      isModalActive: false,
    },
    mutations: {
      closeModal (state) {
        state.isModalActive = false
      },
      openModal (state, biddingExemption) {
        state.biddingExemption = biddingExemption
        state.isModalActive = true
      },
      updateBiddingExemptions (state, { data }) {
        // Temporarily showing bidding exemptions only from Porto Alegre
        // Expanding to other territories require few changes in the frontend
        data = data.filter(elem => elem.gazette.territory_id == '4314902')
        state.biddingExemptions = data
      },
    }
  })
}

export default createStore
