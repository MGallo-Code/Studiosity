<template>
    <main>
        <section id="page-topper"><span>Public Study Sets</span></section>
        <h1 class="main-header">Public Study Sets</h1>
        <div class="control-bar">
            <input class="search-input" placeholder="Search (coming soon)" />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div class="sets-list" v-if="public_sets">
            <router-link v-for="set in public_sets" :key="set.id" :to="`/study-set/${set.id}`" class="set-container">
                <button @click.prevent="toggleFavorite(set)" class="square-btn transparent-btn favorite-btn">
                    <font-awesome-icon class="fa-icon" :icon="[(this.$store.state.isAuthenticated && set.favorited) ? 'fas' : 'far', 'star']"/>
                </button>
                <div>
                    <h2>{{ set.title }}</h2>
                    <p>{{ set.description || "No description provided." }}</p>
                </div>
            </router-link>
        </div>
        <div class="pagination">
            <button @click="navigatePage('previous')" :disabled="!pagination_links.previous">Previous</button>
            <span>Page {{ current_page }} of {{ total_pages }}</span>
            <button @click="navigatePage('next')" :disabled="!pagination_links.next">Next</button>
        </div>
    </main>
</template>

<script>
import { axiosDefaultInstance, axiosAuthInstance } from '../utils/axiosConfig';
import store from "../utils/store";
import router from "../utils/router";

export default {
    data() {
        return {
            error: null,
            public_sets: null,
            pagination_links: {},
            current_page: 1,
            total_pages: 1,
        };
    },
    methods: {
        async getPublicStudySets(page) {
            this.error = null;

            try {
                const response = await axiosDefaultInstance.get(`study_sets/public_sets/?page=${page}`);
                this.public_sets = response.data.results;
                this.pagination_links = response.data.links;
                this.current_page = response.data.current_page;
                this.total_pages = response.data.total_pages;
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred';
            }
        },
        navigatePage(direction) {
            const nextPage = direction === 'next' ? this.current_page + 1 : this.current_page - 1;
            this.$router.push({ path: '/public-study-sets/' + nextPage.toString() });
        },
        // Toggle favorite/unfavorite for a study set
        toggleFavorite(set) {
            // 1) Immediately check if user is authenticated
            if (!store.state.isAuthenticated) {
                // 2) Redirect if not logged in
                router.push('/login');
                return;
            }
            
            // 3) If user is authenticated, proceed with favorite/unfavorite
            axiosAuthInstance.post(`/study_sets/${set.id}/favorite/`)
                .then(response => {
                    set.favorited = response.data.status === 'favorited';
                })
                .catch(error => {
                    console.error("Error toggling favorite status:", error.response ? error.response.data : error);
                });
        },
    },
    watch: {
        '$route.params.page': {
            immediate: true,
            handler(newPage) {
                this.getPublicStudySets(newPage || 1);
            }
        }
    },
    mounted() {
        const initialPage = this.$route.params.page || 1;
        this.getPublicStudySets(initialPage);
    }
}
</script>

<style scoped>
/* List container for sets */

.sets-list {
    background-color: var(--clr-primary-250);
}

/* Level 1 container of set information */
/* SET VIEW (a block) */

.set-container {
    display: flex;
    gap: var(--text-padding-400);
    width: 100%;
    padding: var(--text-padding-400);
    border: 1px solid var(--clr-neutral-300);
    background-color: var(--clr-neutral-50);
    align-items: center;
    text-align: left;
}

/* Level 2 container of set information, holds display information
    - Set display should grow to cover empty space between buttons */

.set-container div {
    flex-grow: 1;
}

/* Make sure display doesn't push list item off of screen */

.set-container:not(.set-creator) div {
    max-width: calc(100% - var(--text-padding-400) - var(--default-btn-size));
}

/* Color in the favorite button */

.favorite-btn {
    color: var(--clr-util-warning);
}

/* Make sure set title doesn't wrap, style... */

.set-container h2 {
    overflow: hidden;
    white-space: nowrap;
    color: var(--clr-neutral-1000);
    font-size: var(--fs-500);
    font-weight: var(--fw-semi-bold);
}

/* Keep description within specific height bounds, style... */

.set-container p {
    overflow: hidden;
    line-height: var(--text-padding-600);
    max-height: 3.2rem;
    padding-left: 0.25rem;
    color: var(--clr-primary-900);
    font-size: var(--fs-300);
}

/* When <main> is at least: DESKTOP MEDIA QUERY */
@container (min-width: 1000px) {
    /* List container for sets */

    .sets-list {
        padding-left: 13%;
        padding-right: 13%;
    }
}
</style>