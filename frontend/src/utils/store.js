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
        // This action can be triggered after login/logout API calls
        updateAuthState({ commit }, isAuthenticated) {
            commit("setAuthentication", isAuthenticated);
        },
    },
});
