<template>
    <div class="login-container">
      <form @submit.prevent="handleLogin">
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
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        loginForm: {
          email: '',
          password: ''
        }
      };
    },
    methods: {
      ...mapActions(['login']),
      async handleLogin() {
        try {
          const response = await axios.post('http://localhost:8000/api/token/', this.loginForm);
          // Handle response, store token, etc.
          this.login(response.data); // Vuex action to update the auth state
          this.$router.push('/'); // Redirect to home or another page
        } catch (error) {
          // Handle error (e.g., display login error message)
          console.error(error);
        }
      }
    }
  }
  </script>
  
  <!-- Add styles as needed -->
  <style>
  /* Your CSS here */
  </style>