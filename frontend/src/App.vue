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

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Open+Sans|Roboto');

:root {
    --clr-primary: rgb(37, 119, 62);
    --clr-primary-dark: #014421;
    --clr-primary-light: #669966;
    --clr-tertiary: #966a9f;
    --clr-tertiary-dark: #5d3965;
    --clr-tertiary-light: #b48ebc;

    --clr-bg: #fffdf4;
    --clr-bg-dark: #edebe5;
    --clr-bg-complement: #faf4d9;

    --clr-text-light: #fffdf4;
    --clr-text-dark: #191814;

    // Utility colors for feedback
    --clr-util-success: #4CAF50; // Success green
    --clr-util-error: #f44336; // Error red
    --clr-util-warning: #deb820; // Warning yellow
    --clr-util-info: #6db0d2; // Information blue
    --clr-util-neutral: #969696; // Neutral gray

    --default-btn-width: 3rem;
    --default-btn-height: 3rem;
    --text-padding-small: 0.6rem;
    --text-padding-med: 1rem;
    --text-padding-lg: 1.2rem;
    --default-border-radius: 7.5px;

    // Typography
    --font-primary: 'Inter', sans-serif;
    --font-secondary: 'Nunito', sans-serif;

    --default-font-size: 1.6rem;

    // Transition

    --default-transition: all 0.1s ease-in-out;
}


#app {
    font-family: var(--font-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: var(--clr-text-dark);
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
    display: block;
    float: inline-start;
    clear: both;
    color: var(--clr-util-error);
    text-align: center;
    padding: --text-padding-small
}

/* Default Button */
.default-btn {
    height: var(--default-btn-height);
    cursor: pointer;
    background-color: var(--clr-primary);
}

/* Stacked Buttons */
.btn-stack {
    display: flex;
    padding: 0;
    width: min-content;
    flex-direction: column;
}

.btn-stack button {
    margin-bottom: 0.2rem;
}

/* Default Square Button */
.square-btn {
    width: var(--default-btn-width);
    height: var(--default-btn-height);
    min-width: var(--default-btn-width);
    min-height: var(--default-btn-height);
    border: none;
    border-radius: var(--default-border-radius);
    cursor: pointer;
    color: var(--clr-text-light);
}

.btn-stack .square-btn {
    transition: var(--default-transition);
}

.btn-stack .square-btn:hover {
    transform: translateX(-0.25em) scale(1.06);
}

.green-btn {
    background-color: var(--clr-util-success) !important;
}

.blue-btn {
    background-color: var(--clr-util-info) !important;
}

.gray-btn {
    background-color: var(--clr-util-neutral) !important;
}

.yellow-btn {
    background-color: var(--clr-util-warning) !important;
}

.red-btn {
    background-color: var(--clr-util-error) !important;
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
    background-color: var(--clr-primary);
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