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
    --clr-btn-gray: #969696;
    --clr-btn-blue: #6db0d2;
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

.square-btn:hover {
    opacity: 0.8;
}

.green-btn {
    background-color: var(--clr-btn-green) !important;
}

.blue-btn {
    background-color: var(--clr-btn-blue) !important;
}

.gray-btn {
    background-color: var(--clr-btn-gray) !important;
}

.yellow-btn {
    background-color: var(--clr-btn-yellow) !important;
}

.red-btn {
    background-color: var(--clr-error) !important;
}

/* Pagination */

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.pagination button {
    margin: 0 5px;
    padding: 5px 10px;
    font-size: 1em;
    border: none;
    border-radius: 5px;
    background-color: var(--clr-base-primary);
    color: white;
    cursor: pointer;
}

.pagination button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

/* font-awesome */

.font-awesome-icon {
    font-size: 1.2em;
}
</style>
