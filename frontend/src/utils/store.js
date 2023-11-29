import { createStore } from "vuex";
import { axiosAuthInstance } from "@/utils/axios-config";

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
        async checkAuthState({ commit }) {
            try {
                await axiosAuthInstance.get("/users/is_authorized/");
                commit("setAuthentication", true);
            } catch (error) {
                commit("setAuthentication", false);
            }
        },
        login({ commit }) {
            commit("setAuthentication", true);
        },
        logout({ commit }) {
            commit("setAuthentication", false);
        },
    },
});
