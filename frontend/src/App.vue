<template>
  <NavbarComponent/>
  <router-view/>
</template>

<script>
import NavbarComponent from './components/NavbarComponent.vue'

export default {
  name: 'App',
  components: {
    NavbarComponent
  }
}
</script>

<style>
:root {
    --clr-base-primary: rgb(50, 129, 75);
    --clr-btn-green: #4CAF50;
    --clr-btn-yellow: #cdae30;
    --clr-error: #f44336;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

@font-face {
    font-family: 'BreeSerif';
    src: url('~@/assets/fonts/BreeSerif-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  text-decoration: none;
}

body {
  width: 100%;
}

.error-message {
    float: inline-start;
    clear: both;
    color: var(--clr-error);
    text-align: center;
}

/* Buttons */

.btn-stack {
    display: flex;
    padding: 0;
    margin-left: 1rem;
    width: min-content;
    flex-direction: column;
}

.btn-stack button {
    margin-bottom: 0.2rem;
}

.square-btn {
    width: 3rem;
    height: 3rem;
    min-width: 3rem;
    min-height: 3rem;
    border: none;
    border-radius: 0.35rem;
    cursor: pointer;
    color: white;
}

.green-btn {
    background-color: var(--clr-btn-green) !important;
}

.yellow-btn {
    background-color: var(--clr-btn-yellow)
}

.red-btn {
    background-color: var(--clr-error) !important;
}

</style>
