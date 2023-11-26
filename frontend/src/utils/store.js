import { createStore } from "vuex";

export default createStore({
    state: {
        isAuthenticated: false,
    },
    mutations: {
        setAuthentication(state, status) {
            state.isAuthenticated = status;
        },
    },
    actions: {
        checkAuthState({ commit }) {
            const token = localStorage.getItem("token");
            if (token) {
                commit("setAuthentication", true);
            } else {
                commit("setAuthentication", false);
            }
        },
        login({ commit }, tokenData) {
            console.log(tokenData.access);
            localStorage.setItem("token", tokenData.access); // Store the token
            commit("setAuthentication", true);
        },
        logout({ commit }) {
            localStorage.removeItem("token"); // Clear token
            commit("setAuthentication", false);
        },
    },
});
