<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <router-link to="/">Studiosity</router-link>
        </div>
        <ul class="navbar-menu">
            <li v-for="item in menuItems" :key="item.text" class="navbar-link">
                <router-link :to="item.link">{{ item.text }}</router-link>
            </li>
            <li v-if="!isAuthenticated">
                <router-link to="/login">Login</router-link>
            </li>
            <li v-if="isAuthenticated" class="profile-picture" @mouseenter="toggleSubMenu(true)"
                @mouseleave="toggleSubMenu(false)">
                <router-link to="/my-profile">
                    <span>{{ this.username }}</span>
                    <img :src="profileImage" alt="Profile" class="profile-pic">
                </router-link>
                <div class="profile-submenu" v-show="showSubMenu">
                    <router-link to="/my-profile">Profile</router-link>
                    <a href="#" @click="handleLogout">
                        <span>Logout&nbsp;&nbsp;<font-awesome-icon :icon="['fas', 'right-from-bracket']" /></span>
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
                        this.profileImage = response.data.profile_image.file_path;
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
:root {
    /* Overall navbar variables */

    --navbar-height: 5rem;
    --navbar-padding: 1rem;

    /* Navbar logo/brand */

    --navbar-logo-margin-right: 1rem;
    --navbar-logo-font-size: 1.35rem;

    /* Navbar links */

    --navbar-link-font-size: 1.3rem;
    /* For horizontal spacing between links */
    --navbar-link-padding: 0 var(--text-padding-med);

    /* Profile picture */

    /* Left margin of profile image WITHIN user name a/router link */
    --profile-pic-left-margin: 0.5rem;
    /* Width + height of profile image in link */
    --profile-pic-size: 2.2rem;
}

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: var(--navbar-height);
    font-size: var(--navbar-font-size);
    font-family: var(--font-secondary);
    background-color: var(--clr-primary);
    color: var(--clr-text-light);
}

.navbar-brand {
    margin: 0 1rem;
    font-size: var(--navbar-logo-font-size);
}

.navbar-menu {
    display: inline-block;
    height: 100%;
}

.navbar-menu li {
    display: inline-block;
    height: 100%;
    width: auto;
}

.navbar-brand a {
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: var(--clr-text-light);
    font-weight: 800;
}

.navbar-menu a {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--navbar-link-padding);
    width: 100%;
    height: 100%;
    text-decoration: none;
    color: var(--clr-text-light);
}

.navbar a:hover,
.navbar a:focus {
    background-color: var(--clr-primary-light);
}

.profile-pic {
    width: var(--profile-pic-size);
    height: var(--profile-pic-size);
    border-radius: 50%;
    margin-left: var(--profile-pic-left-margin);
}

.profile-picture {
    position: relative;
}

.profile-submenu {
    display: inline-block;
    position: absolute;
    right: 0;
    top: var(--navbar-height);
    width: 100%;
    background-color: var(--clr-primary);
    border: 2px solid var(--clr-primary-light);
    box-shadow: 0 2px 5px var(--clr-util-neutral);
    z-index: 100;
}

.profile-submenu a {
    display: flex;
    align-items: center;
    justify-content: center;
    height: var(--navbar-height);
    text-decoration: none;
    color: var(--clr-text-light);
}

.profile-submenu a:hover {
    background-color: var(--clr-primary-light);
}

.profile-submenu a:first-child {
    border-bottom: 2px solid var(--clr-primary-light);
}
</style>