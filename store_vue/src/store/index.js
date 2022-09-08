import { createStore } from 'vuex'

export default createStore({
  state: {
    cart:{
      items:[],
    },
    isAuthenticated: false,
    token:'',
    isLoading:false,
    errors: [],
    infos: [],
    errorTimeoutID: null,
    infoTimeoutID: null

  },
  mutations: {
    initializeStore(state){
      state.errors = []
      state.infos = []
      if (localStorage.getItem('cart')){
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else{
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
      if (localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    addToCart(state, item){
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)
      if (exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else{
        state.cart.items.push(item)
      }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setIsLoading(state, status){
      state.isLoading = status
    },
    setToken(state, token){
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state){
      state.token = ''
      state.isAuthenticated = false
    },
    clearCart(state){
      state.cart = { items: [] }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    addError(state, error){
      state.errors.push(error)
    },
    clearErrors(state){
      if (state.errorTimeoutID){
        clearTimeout(state.errorTimeoutID)
      }
      state.errors = []
    },
    addInfo(state, info){
      state.infos.push(info)
    },
    clearInfos(state){
      if (state.infoTimeoutID){
        clearTimeout(state.infoTimeoutID)
      }
      state.infos = []
    }
  },
 
  actions: {
    dispatchError({ commit, state }, error){
      commit('addError', error)
        state.errorTimeoutID = setTimeout(() => {
        commit('clearErrors')
      }, 5000);
    },
    dispatchInfo({ commit, state }, info){
      commit('addInfo', info)
        state.infoTimeoutID = setTimeout(() => {
        commit('clearInfos')
      }, 10000);
    }
  },
  modules: {
  }
})
