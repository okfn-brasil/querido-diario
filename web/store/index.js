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
        state.biddingExemptions = data
      },
    }
  })
}

export default createStore
