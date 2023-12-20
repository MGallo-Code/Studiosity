<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <router-link to="/">LifeLocker</router-link>
        </div>
        <ul class="navbar-menu">
            <li v-for="item in menuItems" :key="item.text" class="navbar-link">
                <router-link :to="item.link">{{ item.text }}</router-link>
            </li>
            <li v-if="!isAuthenticated">
                <router-link to="/login">Login</router-link>
            </li>
            <li v-if="isAuthenticated" class="profile-picture" @mouseenter="toggleSubMenu(true)" @mouseleave="toggleSubMenu(false)">
                <router-link to="/profile">
                <span>{{ this.username }}</span>
                <img :src="profileImage" alt="Profile" class="profile-pic">
                </router-link>
                <div class="profile-submenu" v-show="showSubMenu">
                    <a href="#" @click="handleLogout">
                        <span>Logout</span>
                    </a>
                </div>
            </li>
        </ul>
    </nav>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { mapState, mapActions } from 'vuex';
import DefaultProfile from '@/assets/default-profile-picture.png';

export default {
    name: "NavbarComponent",
    data() {
        return {
            showSubMenu: false,
            menuItems: [
                { text: "Public Sets", link: "/public-study-sets" },
                { text: "My Sets", link: "/my-study-sets" },
            ],
            profileImage: DefaultProfile,
            username: "",
        };
    },
    computed: {
        ...mapState(['isAuthenticated'])
    },
    methods: {
        toggleSubMenu(state) {
            this.showSubMenu = state;
        },
        ...mapActions(['logout']),
        async getUserProfile() {
            if (this.$store.state.isAuthenticated) {
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
    watch: {
        isAuthenticated(newValue) {
            if (newValue) {
                this.getUserProfile();
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
    height: 5rem;
    font-size: 1.3rem;
    font-family: 'BreeSerif', serif;
    background-color: var(--clr-base-primary);
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
    text-decoration: none;
    color: white;
}

.navbar a:hover {
    background-color: rgb(81, 160, 106);
}

.profile-pic {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-left: 10px;
}

.profile-picture {
    position: relative;
}

.profile-submenu {
    display: inline-block;
    position: absolute;
    right: 0;
    top: 100%;
    width: 100%;
    height: 100%;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
    box-sizing: border-box;
    z-index: 100;
}

.profile-submenu a {
    display: flex;
    align-items: center;
    width: 100%;
    color: black;
    text-decoration: none;
}

.profile-submenu a:hover {
    background-color: #f0f0f0;
}
</style>
