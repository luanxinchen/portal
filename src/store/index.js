import {createStore} from 'vuex'

export default createStore({
    state: {
        id: localStorage.getItem('id') || "",
        name: localStorage.getItem('name') || "",
        token: localStorage.getItem('token') || "",
        role: localStorage.getItem('role') || "",
    },
    getters: {},
    mutations: {
        login(state, {id, name, token,role}) {
            state.id = id;
            state.name = name;
            state.token = token;
            state.role = role;

            localStorage.setItem('id', id);
            localStorage.setItem('name', name);
            localStorage.setItem('token', token);
            localStorage.setItem('role', role);
        },
        logout(state) {
            state.id = "";
            state.name = "";
            state.token = "";
            state.role = "";
            localStorage.removeItem('id');
            localStorage.removeItem('name');
            localStorage.removeItem('token');
            localStorage.removeItem('role');
        },
    },
    actions: {},
    modules: {}
})
