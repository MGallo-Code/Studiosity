<template>
    <div class="set-detail-container">
        <h1>{{ setDetail.title }}</h1>
        <p>{{ setDetail.description || 'No description provided.' }}</p>

        <div class="study-terms">
            <h2>Study Terms</h2>
            <div v-for="term in studyTerms" :key="term.id" class="term-item">
                <div><strong>Front:</strong> {{ term.front_text }}</div>
                <div><strong>Back:</strong> {{ term.back_text }}</div>
                <!-- Display images, audio, and tags if available -->
            </div>
        </div>
    </div>
</template>

<script>
import { axiosDefaultInstance } from '../utils/axios-config';

export default {
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
                const setResponse = await axiosDefaultInstance.get(`study_sets/sets/${setId}/`);
                this.setDetail = setResponse.data;
                const termsResponse = await axiosDefaultInstance.get(`study_sets/terms_in_set/${setId}/`);
                this.studyTerms = termsResponse.data;
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred';
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
