<template>
    <main>
        <section id="page-topper">Viewing Set: {{ setDetail.title }}</section>
        <div class="main-header set-banner">
            <button @click="toggleFavorite" class="square-btn favorite-btn transparent-btn"><font-awesome-icon class="fa-icon"
                    :icon="[(this.$store.state.isAuthenticated && setDetail.favorited) ? 'fas' : 'far', 'star']" /></button>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </div>
        <FlashcardViewerComponent
            v-if="showFlashcards"
            :cards="studyTerms"
            @close="showFlashcards = false"
        />
        <button @click="showFlashcards = true">Show Flashcards</button>
        <section class="terms-list">
            <!-- Iterating over each term to display -->
            <div v-for="term in studyTerms" :key="term.id" class="term-info-display">
                <div class="img-info-flow">
                    <picture v-if="term.front_image">
                        <img :src="term.front_image.file_path" />
                    </picture>
                    <span @click="speak('front', term)">
                        <p>{{ term.front_text }}</p>
                    </span>
                </div>
                <div class="img-info-flow">
                    <picture v-if="term.back_image">
                        <img :src="term.back_image.file_path" />
                    </picture>
                    <span @click="speak('back', term)">
                        <p>{{ term.back_text }}</p>
                    </span>
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import store from "../utils/store";
import router from "../utils/router";
import FlashcardViewerComponent from './FlashcardViewerComponent.vue';

export default {
    components: {
        PlayTermsComponent,
        FlashcardViewerComponent
    },
    data() {
        return {
            setDetail: {},
            studyTerms: [],
            showFlashcards: false,
            error: null,
        };
    },
    created() {
        this.fetchSetDetail();
    },
    methods: {
        async fetchSetDetail() {
            try {
                const setId = this.$route.params.id;
                const response = await axiosAuthInstance.get(`study_sets/public_sets/${setId}/`);
                // Separate terms and the rest of set details
                const { terms, ...setDetails } = response.data;
                this.setDetail = setDetails;
                // Sort our response by sort_order
                terms.sort((a, b) => a.sort_order - b.sort_order);
                this.studyTerms = terms;
            } catch (error) {
                // If set not found (no permission)
                if (error.response && error.response.data.detail === "Not found.") {
                    this.$router.push({ path: '/public-study-sets/' })
                } else {
                    // If set not found (no permission)
                    if (error.response && error.response.data.detail === "Not found.") {
                        this.$router.push({ path: '/my-study-sets/' })
                    } else {
                        this.error = error.response ? error.response.data.detail : 'An error occurred';
                    }
                }
            }
        },
        // Toggle favorite/unfavorite for a study set
        toggleFavorite() {
            // 1) Immediately check if user is authenticated
            if (!store.state.isAuthenticated) {
                // 2) Redirect if not logged in
                router.push('/login');
                return;
            }
            
            // 3) If user is authenticated, proceed with favorite/unfavorite
            axiosAuthInstance.post(`/study_sets/${this.setDetail.id}/favorite/`)
                .then(response => {
                    this.setDetail.favorited = response.data.status === 'favorited';
                })
                .catch(error => {
                    console.error("Error toggling favorite status:", error.response ? error.response.data : error);
                });
        },
    }
};
</script>

<style>
/* SET BANNER */

/* Main div holding set information/edit sections */
.set-banner {
    position: relative;
}

/* Targets favorite button in set-banner display, overrides rules above */
.set-banner .favorite-btn {
    position: absolute;
    top: var(--text-padding-400) !important;
    left: var(--text-padding-400) !important;
    margin-right: var(--text-padding-400);
}

/* Set title */
.set-banner h1 {
    padding: var(--text-padding-400) var(--text-padding-1100) 0 var(--text-padding-1100);
}

/* Set description */
.set-banner p {
    padding: var(--text-padding-250) var(--text-padding-1000) var(--text-padding-400) var(--text-padding-1000);
}

/* SET TERMS */

/* Set background outside of terms list */
.terms-list {
    background-color: var(--clr-primary-250);
}

/* Level 1 term container contains:
    2x .img-info-flow
*/
.term-info-display {
    display: flex;
    flex-direction: row;
    gap: var(--text-padding-400);
    width: 100%;
    border-bottom: 1px solid var(--clr-neutral-300);
    background-color: var(--clr-neutral-50);
}

/* Level 2 term container, separates text from image */
.img-info-flow {
    flex: 0 0 calc(50% - (var(--text-padding-400) / 2));
    display: flex;
    flex-direction: column;
    max-width: 100%;
    overflow: hidden;
    align-items: center;
}

/* Term images */
.term-info-display picture {
    position: relative;
    max-width: 100%;
    width: 12rem;
    height: 12rem;
}

.term-info-display img {
    width: 100%;
    height: 100%;
    overflow: hidden;
    object-fit: cover;
    border-radius: 12px;
    border: 2px solid var(--clr-base-primary);
}

/* When <main> is at least */
@container (min-width: 1000px) {
    /* Give terms list some spacing on large main width */
    .terms-list {
        padding-left: 13%;
        padding-right: 13%;
    }
}
</style>