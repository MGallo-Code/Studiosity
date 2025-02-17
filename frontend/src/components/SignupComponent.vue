<template>
    <main class="signup-container">
        <section id="page-topper"><span>Sign up</span></section>
        <h1 class="main-header">Create a New Account</h1>
        <form class="signup-form" @submit.prevent="handleSignup">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="signupForm.username" required>
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="signupForm.email" autocomplete="email" required>
            <label for="email2">Confirm Email:</label>
            <input type="email" id="email2" v-model="signupForm.email2" autocomplete="email" required>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="signupForm.password" autocomplete="" required>
            <label for="password2">Confirm Password:</label>
            <input type="password" id="password2" v-model="signupForm.password2" autocomplete="" required>
            <div v-if="error" class="error-message">{{ error }}</div>
            <button type="submit">Sign Up</button>
        </form>
    </main>
</template>

<script>
import { axiosDefaultInstance } from '../utils/axiosConfig';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        return {
            signupForm: {
                username: '',
                email: '',
                email2: '',
                password: '',
                password2: '',
            },
            error: null,
        };
    },
    methods: {
        async handleSignup() {
            // Reset error on new submission
            this.error = null;

            // Check if passwords and emails match
            if (this.signupForm.password !== this.signupForm.password2) {
                this.error = "Passwords do not match.";
                return;
            }
            if (this.signupForm.email !== this.signupForm.email2) {
                this.error = "Email addresses do not match.";
                return;
            }

            try {
                await axiosDefaultInstance.post('users/create/', this.signupForm);
                this.$router.push('/login');
            } catch (error) {
                let errorMsg = extractFirstErrorMessage(error);
                if (errorMsg === "user model with this username already exists.") {
                    this.error = "This username is already in use. Please try another."
                } else if (errorMsg === "user model with this email already exists.") {
                    this.error = "This email is already in use. If this is your account, please try resetting your password."
                } else {
                    this.error = errorMsg;
                }
            }
        }
    }
}
</script>
  
<style>
.signup-form {
    display: grid;
    place-items: center;
    grid-template-columns: 1fr 2fr;
    grid-template-rows: auto;
    row-gap: var(--text-padding-200);
    width: 80%;
    margin: 20px auto;
}

.signup-form label {
    grid-column: 1;
    width: 100%;
    text-align: right;
    font-weight: var(--fw-semi-bold);
}

.signup-form input {
    grid-column: 2;
    width: 80%;
    /* Adopt base font styling & border from your design tokens */
    padding: var(--text-padding-250);
    border: 1px solid var(--clr-neutral-300);
    border-radius: var(--default-border-radius);
    font-size: var(--fs-400);
    font-family: var(--ff-body);
}

.error-message {
    grid-column: 1 / 3;
    text-align: center;
    color: var(--clr-util-error);
    padding: var(--text-padding-300);
}

.signup-form button {
    /* Spans both columns */
    grid-column: 1 / 3;
    width: 50%;
    margin-top: var(--text-padding-300);

    /* Visual style from base tokens */
    background-color: var(--clr-primary-600);
    color: var(--clr-neutral-0);
    font-size: var(--fs-button);
    font-weight: var(--fw-bold);
    border-radius: var(--default-border-radius);
    border: none;
    cursor: pointer;
    height: var(--default-btn-size);
}
</style>