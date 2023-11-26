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
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        signupForm: {
          username: '',
          email: '',
          email2: '',
          password: '',
          password2: '',
        }
      };
    },
    methods: {
      async handleSignup() {
        // if passmatch
        try {
          const response = await axios.post('http://localhost:8000/api/users/create/', this.signupForm);
          console.log(response);
          this.$router.push('/login'); // Redirect to home or another page
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
  </style>