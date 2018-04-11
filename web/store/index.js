import Vuex from 'vuex'

const createStore = () => {
  return new Vuex.Store({
    state: {
        biddingExemptions: []
    },
    mutations: {
        updateBiddingExemptions (state, { data }) {
            state.biddingExemptions = data
      }
    }
  })
}

export default createStore
