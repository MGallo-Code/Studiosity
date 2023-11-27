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
                <a href="#" @click="handleLogout">Logout</a>
            </li>
        </ul>
    </nav>
</template>

<script>
import axiosInstance from '../utils/axios-config';
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
        async handleLogout() {
        try {
          await axiosInstance.post('/logout/');
          this.$store.dispatch('updateAuthState', false);
          this.$router.push('/login');
        } catch (error) {
            if (error.response && error.response.data.detail) {
                console.log("Error: ", error.response.data.detail);
            } else {
                console.log("An unknown error occurred while signing up.");
            }
        }
      }
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
