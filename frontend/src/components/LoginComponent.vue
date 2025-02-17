<template>
    <main>
        <section id="page-topper"><span>Log in</span></section>
        <h1 class="main-header">Log Into an Existing Account</h1>
        <section class="login-container">
            <form @submit.prevent="handleLogin">
                <div v-if="error" class="error-message">{{ error }}</div>

                <div class="form-group">
                    <label for="email">Email:</label>
                    <input
                    type="email"
                    id="email"
                    v-model="loginForm.email"
                    autocomplete="email"
                    required
                    />
                </div>

                <div class="form-group">
                    <label for="password">Password:</label>
                    <input
                    type="password"
                    id="password"
                    v-model="loginForm.password"
                    autocomplete="current-password"
                    required
                    />
                </div>

                <button type="submit">Login</button>
            </form>

            <p class="signup-prompt">
            No account? Click
            <router-link to="/signup">here</router-link>
            to register.
            </p>
        </section>
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
    error: null
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
        this.error =
        error.response?.data?.detail || 'An unknown error occurred while logging in.';
    }
    }
}
};
</script>

<style scoped>
/* Container for the login page */
.login-container {
    /* Center the content and limit its maximum width */
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: var(--text-padding-700) var(--text-padding-400);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--text-padding-400);
    background-color: var(--clr-neutral-0);
}

/* The login form styling */
form {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: var(--text-padding-300);
}

/* Label and input grouping */
.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

/* Basic label styling */
.form-group label {
    font-weight: var(--fw-semi-bold);
}

/* Inputs adopt base font style */
.form-group input {
    padding: var(--text-padding-250);
    border: 1px solid var(--clr-neutral-300);
    border-radius: var(--default-border-radius);
    font-size: var(--fs-400);
    font-family: var(--ff-body);
}

/* The login button picks up default button styles, color it. */
button[type='submit'] {
    background-color: var(--clr-primary-600);
    color: var(--clr-neutral-0);
    font-size: var(--fs-button);
    font-weight: var(--fw-bold);
}

/* Paragraph prompting user to sign up */
.signup-prompt {
    margin-top: var(--text-padding-400);
    text-align: center;
}

/* Minor style for the router-link to look clickable */
.signup-prompt a {
    color: var(--clr-primary-700);
    text-decoration: underline;
}
</style>