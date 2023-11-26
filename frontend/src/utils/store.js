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
            localStorage.setItem("token", tokenData.access);
            localStorage.setItem("refresh_token", tokenData.refresh);
            commit("setAuthentication", true);
        },
        logout({ commit }) {
            localStorage.removeItem("token");
            localStorage.removeItem("refresh_token");
            commit("setAuthentication", false);
        },
    },
});
