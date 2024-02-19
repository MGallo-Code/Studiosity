<template>
    <NavbarComponent />
    <router-view />
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
@import url('./styles/reset.css');
@import url('./styles/base-style.css');
@import url('https://fonts.googleapis.com/css?family=Open+Sans|Roboto');

#app {
    font-family: var(--font-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: var(--clr-text-dark);
}
</style>