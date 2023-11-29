<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <a href="/">LifeLocker</a>
        </div>
        <ul class="navbar-menu">
            <li v-for="item in menuItems" :key="item.text" class="navbar-link">
                <router-link :to="item.link">{{ item.text }}</router-link>
            </li>
            <li v-if="!isAuthenticated">
                <router-link to="/login">Login</router-link>
            </li>
            <li v-else class="profile-picture">
                <img :src="profileImage" alt="Profile" class="profile-pic">
            </li>
            <li v-if="isAuthenticated">
                <a href="#" @click="handleLogout">Logout</a>
            </li>
        </ul>
    </nav>
</template>

<script>
import { axiosAuthInstance } from '../utils/axios-config';
import { mapState, mapActions } from 'vuex';

import DefaultProfile from '@/assets/default-profile.png';

export default {
    name: "NavbarComponent",
    data() {
        return {
            menuItems: [
                { text: "Public Study Sets", link: "/public-study-sets" },
                { text: "My Study Sets", link: "/my-study-sets" },
            ],
            profileImage: DefaultProfile,
            username: "",
        };
    },
    computed: {
        ...mapState(['isAuthenticated'])
    },
    methods: {
        ...mapActions(['logout']),
        async getUserProfile() {
            if (this.$store.isAuthenticated) {
                try {
                    const response = await axiosAuthInstance.get('/users/profile/');
                    if (response.data.profile_image) {
                        this.profileImage = response.data.profile_image;
                    }
                    this.username = response.data.username;
                } catch (error) {
                    if (error.response && error.response.data.detail) {
                        console.log("Error getting profile: ", error.response.data.detail);
                    } else {
                        console.log("An unknown error occurred getting profile.");
                    }
                }
            }
        },
        async handleLogout() {
            try {
                await axiosAuthInstance.post('/logout/');
                this.$store.dispatch('logout');
                this.$router.push('/login');
            } catch (error) {
                if (error.response && error.response.data.detail) {
                    console.log("Error logging out: ", error.response.data.detail);
                } else {
                    console.log("An unknown error occurred logging out.");
                }
            }
        }
    },
    created() {
        this.getUserProfile();
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

.profile-pic {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
}
</style>
