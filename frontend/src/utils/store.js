import { createStore } from "vuex";
import { axiosAuthInstance } from "@/utils/axiosConfig";

export default createStore({
    state: {
        isAuthenticated: false,
    },
    mutations: {
        setAuthentication(state, status) {
            state.isAuthenticated = status;
            localStorage.setItem('isAuthenticated', status);
        },
    },
    actions: {
        initializeAuthState({ commit }) {
            // Read from localStorage synchronously and update Vuex state
            const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
            commit('setAuthentication', isAuthenticated);
        },
        async validateSession({ commit }) {
            try {
                await axiosAuthInstance.get("/users/is_authorized/");
                // If this succeeds, the user is still authenticated
                commit('setAuthentication', true);
            } catch (error) {
                // If this fails, the user is not authenticated
                commit('setAuthentication', false);
                localStorage.removeItem('isAuthenticated');
            }
        },
        login({ commit }) {
            commit('setAuthentication', true);
        },
        async logout({ commit }) {
            try {
                // Remove httponly cookies with django
                await axiosAuthInstance.post("/logout/");
            } catch (error) {
                console.error("Logout request failed:", JSON.parse(JSON.stringify(error?.response || error)));
            }
            
            // Clear local auth state
            commit("setAuthentication", false);
            localStorage.removeItem("isAuthenticated");
        },
    },
});
