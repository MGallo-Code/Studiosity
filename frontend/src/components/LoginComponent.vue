<template>
    <main class="login-container">
        <section id="page-topper"><span>Log in</span></section>
        <h1 class="main-header">Log Into an Existing Account</h1>
        <form @submit.prevent="handleLogin">
            <div v-if="error" class="error-message">{{ error }}</div>
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="loginForm.email" autocomplete="email" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="loginForm.password" autocomplete="current-password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p>No account? Click <router-link to="/signup">here</router-link> to register.</p>
    </main>
</template>
  
<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            loginForm: {
                email: '',
                password: ''
            },
            error: null,
        };
    },
    methods: {
        ...mapActions(['login']),
        async handleLogin() {
            // Reset error on new submission
            this.error = null;
            try {
                await axiosAuthInstance.post('/token/', this.loginForm, {
                    _ignoreInterceptor: true
                });

                // Update authentication status
                this.$store.dispatch('login');

                const redirect = this.$route.query.redirect || '/';
                this.$router.push(redirect);
            } catch (error) {
                this.error = error.response?.data?.detail || "An unknown error occurred while logging in.";
            }
        }
    }
}
</script>
  
  <!-- Add styles as needed -->
<style>
/* Your CSS here */
</style>