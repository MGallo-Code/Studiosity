<template>
  <div class="signup-container">
    <form @submit.prevent="handleSignup">
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
  </div>
</template>

<script>
import { axiosDefaultInstance } from '../utils/axios-config';

export default {
  data() {
    return {
      signup_form: {
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
      if (this.signup_form.password !== this.signup_form.password2) {
        this.error = "Passwords do not match.";
        return;
      }
      if (this.signup_form.email !== this.signup_form.email2) {
        this.error = "Email addresses do not match.";
        return;
      }

      try {
        await axiosDefaultInstance.post('users/create/', this.signup_form);
        this.$router.push('/login');
      } catch (error) {
        if (error.response.data.username) {
          this.error = "This username is taken.";
        } else if (error.response.data.email) {
          this.error = "This email is taken.";
        } else {
          this.error = "An unknown error occurred while signing up.";
        }
      }
    }
  }
}
</script>
  
<style>
form {
  display: grid;
  place-items: center;
  grid-template-columns: 1fr 2fr;
  grid-template-rows: auto;
  row-gap: 0.3rem;
  width: 80%;
  margin: 0 auto;
}
label {
  grid-column: 1;
  width: 100%;
  text-align: right;
}
input {
  grid-column: 2;
  width: 80%;
}
button {
  width: 50%;
  grid-column: 1 / 3
}
.error-message {
  grid-column: 1 / 3;
  text-align: center;
}
</style>