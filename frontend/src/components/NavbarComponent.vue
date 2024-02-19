<template>
    <header :class="['primary-header', { 'is-open': navIsOpen }]">
        <button class="square-btn nav-toggle" @click="toggleNavigation" aria-controls="primary-navigation"
            :aria-expanded="navIsOpen.toString()">
            <font-awesome-icon :icon="navIsOpen ? ['fas', 'xmark'] : ['fas', 'bars']" class="fa-icon" />
            <span class="visually-hidden">Menu</span>
        </button>
        <div class="nav-container">
            <div class="navbar-brand">
                <router-link to="/">Studiosity</router-link>
            </div>
            <nav class="primary-navigation" id="primary-navigation">
                <ul aria-label="Primary" role="list" class="nav-list">
                    <li><router-link to="/public-study-sets">Public Sets</router-link></li>
                    <li><router-link to="/my-study-sets">My Sets</router-link></li>
                </ul>
                <div v-if="isAuthenticated">
                    <router-link to="/my-profile" class="profile-link">
                        <img :src="profileImage" alt="Profile" class="profile-pic">
                        <span>{{ this.username }}</span>
                        <button class="square-btn" @click="handleLogout">
                            <font-awesome-icon class="fa-icon" :icon="['fas', 'right-from-bracket']" />
                        </button>
                    </router-link>
                </div>
                <div v-else>
                    <router-link to="/login" class="btn square-btn nav-login">Login</router-link>
                </div>
            </nav>
        </div>
    </header>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { mapState, mapActions } from 'vuex';
import DefaultProfile from '@/assets/default-profile-picture.png';

export default {
    name: "NavbarComponent",
    data() {
        return {
            navIsOpen: false,
            profileImage: DefaultProfile,
            username: "",
        };
    },
    computed: {
        ...mapState(['isAuthenticated'])
    },
    methods: {
        toggleNavigation() {
            this.navIsOpen = !this.navIsOpen;
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
            if (newValue) this.getUserProfile();
        }
    },
    created() {
        this.getUserProfile();
    }
};
</script>

<style>
:root {
    /* Custom variables for navigation */
    --nav-desktop-width: 16rem;
    --nav-tablet-width: 70%;
    /* For calculating nav toggle button's position in tablet media query*/
    --nav-tablet-width-pct: 0.7;
    --nav-mobile-width: 100%;
    /* Assume mobile for responsive */
    --nav-width: var(--nav-mobile-width);

    --fs-nav-link: var(--fs-700);
    --fs-nav-username: var(--fs-600);

    --nav-text-color: var(--clr-neutral-0);
    --nav-background-color: var(--clr-primary-700);
    --nav-hover-background-color: var(--clr-primary-300);
    --nav-profile-pic-size: 45px;
    --nav-transition-speed: 0.3s;
}

/* Component's main container, defines size for .nav-container to fill */
/* Problem is it blocks input on the page even when the menu is closed */
.primary-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 0;
    height: 0;
    z-index: 999;
}

/* Assume menu closed, place nav toggle button just outside of left screen for easy access--
    Also style btn...*/
.nav-toggle {
    position: absolute;
    left: 0;
    color: var(--nav-text-color);
    background-color: var(--nav-background-color);
    border-radius: 0;
    transition: left var(--nav-transition-speed) ease-in-out;
    z-index: 1000;
}

/* Set position at which button should take on open nav menu */
.is-open .nav-toggle {
    /* Assume mobile, place on right side of screen */
    left: calc(100vw - var(--magnified-btn-size));
}

/* Main navigation container, which slides left and right as required */
.nav-container {
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    /* Assume mobile, take mobile width */
    width: var(--nav-width);
    height: 100vh;
    justify-content: space-between;
    background-color: var(--nav-background-color);
    z-index: 999;
    /* Initially hide nav-container */
    transform: translateX(-100%);
    transition: transform var(--nav-transition-speed) ease-in-out;
}

/* Move container to accessible position */
.is-open .nav-container {
    transform: translateX(0);
}

/* Styling brand/logo */
.navbar-brand {
    padding: var(--default-btn-size) var(--text-padding-300);
}

.navbar-brand a {
    font-size: var(--fs-700);
    font-weight: var(--fw-bold);
    color: var(--clr-neutral-0);
}

/* Ensure primary-navigation fills the rest of space, set stage for flex */
.primary-navigation {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

/* Make sure .primaty-navigation flex pushes profile-link to the bottom of nav menu */
.nav-list {
    flex-grow: 1;
}

/* Set style for links in navigation */
.nav-list a {
    /* Ensure main nav links are displayed in column, not inline */
    display: block;
    text-align: left;
    font-weight: var(--fw-semi-bold);
    font-size: var(--fs-nav-link);
    color: var(--nav-text-color);
    padding: var(--text-padding-300) 18%;
}

/* TODO */
/* .nav-list li a:hover::after {
    display: inline-block;
    width: 3rem;
    height: 3rem;
    background-color: red;
} */

/* Style login button -- replaces .profile-link when user is unauthenticated */
a.nav-login {
    display: block;
    padding: var(--text-padding-700);
    text-align: center;
    background-color: var(--clr-primary-900);
}

/* Style profile display to show:
    profile-pic, span with username, and logout btn inline */
.profile-link {
    display: flex;
    align-items: center;
    justify-content: left;
    gap: var(--text-padding-600);
    padding: var(--text-padding-600);
    padding-left: var(--text-padding-600);
    background-color: var(--clr-primary-900);
}

/* Set style for span containing username */
.profile-link span {
    /* Ensure that profile name grows to push logout btn to the right */
    flex-grow: 1;
    text-align: left;
    font-weight: var(--fw-semi-bold);
    font-size: var(--fs-nav-username);
    color: var(--nav-text-color);
}

.profile-link span:hover {
    text-decoration: underline;
}

/* Style profile picture within .profile-link */
.profile-pic {
    width: var(--nav-profile-pic-size);
    height: var(--nav-profile-pic-size);
    border-radius: 50%;
}

/* Style logout icon/button */
.profile-link button {
    background-color: var(--clr-primary-900);
}

.profile-link button svg {
    color: var(--clr-neutral-0);
}

.profile-link button:hover {
    background-color: var(--clr-primary-300);
}

.profile-link button:hover svg {
    color: var(--clr-primary-900);
}

/* TABLET + PHONE */
@media screen and (max-width: 767px) {

    /* Make buttons bigger, better visibility */
    .profile-link button,
    .nav-toggle {
        width: 3.2rem !important;
        height: 3.2rem !important;
    }

    .profile-link button svg {
        font-size: var(--fs-500) !important;
    }

    .nav-toggle svg {
        font-size: var(--fs-600) !important;
    }
}

/* TABLET MEDIA QUERY */
@media screen and (min-width: 490px) {
    :root {
        --nav-width: var(--nav-tablet-width);
    }

    /* Set position which nav toggle button should take on open nav menu */
    .is-open .nav-toggle {
        left: calc((100vw * var(--nav-tablet-width-pct)) - var(--magnified-btn-size));
    }
}

/* DESKTOP MEDIA QUERY */
@media screen and (min-width: 768px) {
    :root {
        --fs-nav-link: var(--fs-500);
        --fs-nav-username: var(--fs-400);

        --nav-width: var(--nav-desktop-width);
        --nav-profile-pic-size: 35px;
    }

    /* Set position which nav button should take on open nav menu */
    .is-open .nav-toggle {
        left: calc(var(--nav-desktop-width) - var(--magnified-btn-size));
    }

    /* Set padding to match our new fs */

    .profile-link {
        padding: var(--text-padding-300);
        padding-left: var(--text-padding-500);
        gap: var(--text-padding-500);
    }

    .nav-list a {
        padding: var(--text-padding-300) 20%;
    }
}
</style>