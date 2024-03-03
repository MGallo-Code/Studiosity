<template>
    <main>
        <section id="page-topper">Viewing Set: {{ setDetail.title }}</section>
        <section class="main-header">
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </section>
        <section class="set-detail-container">
            <PlayTermsComponent :studyTerms="studyTerms" v-if="studyTerms.length > 0" />

            <div class="study-terms">
                <div v-for="term in studyTerms" :key="term.id" class="term-item">
                    <div><strong>Front:</strong> {{ term.front_text }}</div>
                    <div><strong>Back:</strong> {{ term.back_text }}</div>
                    <!-- Display images, audio, and tags if available -->
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import PlayTermsComponent from '@/components/PlayTermsComponent.vue';


export default {
    components: {
        PlayTermsComponent
    },
    data() {
        return {
            setDetail: {},
            studyTerms: [],
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
        }
    }
};
</script>

<style>
.set-detail-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

.study-terms {
    margin-top: 20px;
}

.term-item {
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}
</style>
