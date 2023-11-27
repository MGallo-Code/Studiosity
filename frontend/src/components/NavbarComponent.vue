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
import { axiosAuthInstance } from '../utils/axios-config';
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
          await axiosAuthInstance.post('/logout/');
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
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 4rem;
    background-color: rgb(63, 152, 91);
}
.navbar-brand {
    margin: 0 1.5rem;
}
.navbar-menu {
    display: inline-block;
    height: 100%;
}
.navbar-menu li {
    display: inline-block;
    height: 100%;
    width: 10rem;
}
.navbar a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    color: black;
    text-decoration: none;
}

.navbar a:hover {
    background-color: rgb(104, 184, 129);
}
</style>
