<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <a href="/">LifeLocker</a>
        </div>
        <ul class="navbar-menu">
            <li v-for="item in menuItems" :key="item.text">
                <router-link :to="item.link">{{ item.text }}</router-link>
            </li>
            <li v-if="!isAuthenticated">
                <router-link to="/login">Login</router-link>
            </li>
            <li v-else>
                <a href="#" @click="logout">Logout</a>
            </li>
        </ul>
    </nav>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
    name: "NavbarComponent",
    data() {
        return {
            menuItems: [
                { text: "Public Study Sets", link: "/public-study-sets" },
                { text: "My Study Sets", link: "/my-study-sets" },
            ],
        };
    },
    computed: {
        ...mapState(['isAuthenticated'])
    },
    methods: {
        ...mapActions(['logout']),
    }
};
</script>

<style>
/* Add your CSS styling here */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 4rem;
    background-color: lightseagreen;
}
.navbar-brand {
    margin: 0 1.5rem;
}
.navbar-menu {
    margin: 0 1.5rem;
}
.navbar-menu li {
    display: inline-block;
    margin-left: 1rem;
}
</style>
