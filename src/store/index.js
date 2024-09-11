import {createStore} from 'vuex'

export default createStore({
  state: {
    id: localStorage.getItem('id') || "",
    name: localStorage.getItem('name') || "",
    token: localStorage.getItem('token') || "",
  },
  getters: {},
  mutations: {
    login(state, {id, name, token}) {
      state.id = id;
      state.name = name;
      state.token = token;

      localStorage.setItem('id', id);
      localStorage.setItem('name', name);
      localStorage.setItem('token', token);
    },
    logout(state) {
      state.id = "";
      state.name = "";
      state.token = "";
      localStorage.removeItem('id');
      localStorage.removeItem('name');
      localStorage.removeItem('token');
    },
  },
  actions: {},
  modules: {}
})
