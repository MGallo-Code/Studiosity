<template>
    <!-- Editable Study Set Details -->
    <div class="set-banner set-banner-edit" v-if="editingSet">
        <div>
            <p v-if="editSetError" class="error-message">{{ editSetError }}</p>
            <input type="text" v-model="setEditForm.title" />
            <textarea v-model="setEditForm.description"></textarea>
            <select v-model="setEditForm.private">
                <option value="false">Public</option>
                <option value="true">Private</option>
            </select>
        </div>
        <div class="btn-stack">
            <button @click="updateSetDetails" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'check']" /></button>
            <button @click="toggleEditSetDetails" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button>
            <button @click="confirmDeleteSet" class="square-btn red-btn"><font-awesome-icon :icon="['fas', 'trash-alt']" /></button>
        </div>
    </div>
    <div class="set-banner" v-else>
        <button @click="toggleFavorite(setDetail)" class="favorite-btn square-btn"><font-awesome-icon :icon="[setDetail.favorited ? 'fas' : 'far', 'star']" /></button>
        <button @click="toggleEditSetDetails" class="square-btn blue-btn"><font-awesome-icon :icon="['fas', 'edit']" /></button>
        <h1>{{ setDetail.title }}</h1>
        <p>{{ setDetail.description || 'No description provided.' }}</p>
    </div>

    <!-- Study Terms List -->
    <div class="terms-list">
        <!-- Inline form for creating a new term -->
        <div class="term-container new-term-form" v-if="creatingNewTerm">
            <p v-if="createTermError" class="error-message">{{ createTermError }}</p>
            <input type="text" placeholder="Front text" v-model="newTerm.front_text" />
            <input type="text" placeholder="Back text" v-model="newTerm.back_text" />
            <div class="btn-stack">
                <button @click="createTerm" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'plus']" /></button>
                <button @click="toggleCreateNewTerm" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button> 
            </div>
        </div>

        <!-- Button to toggle new term creation form -->
        <button @click="toggleCreateNewTerm" :disabled="creatingNewTerm">Create New Term</button>

        <!-- Iterating over each term to display -->
        <div v-for="term in studyTerms" :key="term.id" class="term-container">
            <!-- Editable term form -->
            <div class="term-display" v-if="editingTerm && editingTerm.id === term.id">
                <p v-if="editTermError" class="error-message">{{ editTermError }}</p>
                <div class="front-back-display">
                    <span>
                        <textarea v-model="termForm.front_text" />
                        <p @click="speak(termForm.front_text)"><font-awesome-icon icon="volume-up" /></p>
                    </span>
                    <div class="spacer"></div>
                    <span>
                        <textarea v-model="termForm.back_text" />
                        <p @click="speak(termForm.back_text)"><font-awesome-icon icon="volume-up" /></p>
                    </span>
                </div>
                <div class="btn-stack">
                    <button @click="updateTerm" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'check']" /></button>
                    <button @click="editTerm(null)" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button>
                    <button @click="confirmDeleteTerm(term.id)" class="square-btn red-btn"><font-awesome-icon :icon="['fas', 'trash-alt']" /></button>
                </div>
            </div>
            <!-- Display term details -->
            <div v-else class="term-display">
                <div class="front-back-display">
                    <span @click="speak(term.front_text)">
                        {{ term.front_text }}
                        <p><font-awesome-icon icon="volume-up" /></p>
                    </span>
                    <div class="spacer"></div>
                    <span @click="speak(term.back_text)">
                        {{ term.back_text }}
                        <p><font-awesome-icon icon="volume-up" /></p>
                    </span>
                </div>
                <button @click="editTerm(term)" class="square-btn blue-btn"><font-awesome-icon :icon="['fas', 'edit']" /></button>
            </div>
        </div>
    </div>
</template>


<script>
import { axiosAuthInstance } from '../utils/axios-config';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        // Initializing data properties
        return {
            setDetail: {},
            setEditForm: {},
            studyTerms: [],
            editSetError: null,
            createTermError: null,
            editTermError: null,
            editingSet: false,
            editingTerm: null,
            termForm: {
                front_text: '',
                back_text: '',
                study_set: null,
            },
            creatingNewTerm: false,
            newTerm: { front_text: '', back_text: '', study_set: null },
        };
    },
    created() {
        // Fetching initial data when component is created
        this.fetchSetDetail();
    },
    methods: {
        // Fetches details of the study set and its terms
        async fetchSetDetail() {
            try {
                const setId = this.$route.params.id;
                this.termForm.study_set = setId;
                const setResponse = await axiosAuthInstance.get(`study_sets/study_sets/${setId}/`);
                this.setDetail = setResponse.data;

                const termsResponse = await axiosAuthInstance.get(`study_sets/terms_in_set/${setId}/`);
                this.studyTerms = termsResponse.data;
            } catch (error) {
                // If set not found (no permission)
                if (error.response && error.response.data.detail === "Not found.") {
                    this.$router.push({ path: '/my-study-sets/' })
                } else {
                    console.log(error.response ? error.response.data.message : 'Error fetching sets');
                }
            }
        },

        toggleEditSetDetails() {
            if (!this.editingSet) {
                // Entering edit mode, make a copy of setDetail
                this.setEditForm = { ...this.setDetail };
            }
            this.editingSet = !this.editingSet;
            this.editSetError = null;
        },

        // Updates study set details
        async updateSetDetails() {
            try {
                await axiosAuthInstance.put(`/study_sets/study_sets/${this.setDetail.id}/`, this.setEditForm);
                this.setDetail = { ...this.setEditForm };
                this.editingSet = false;
                this.fetchSetDetail();
            } catch (error) {
                this.editSetError = extractFirstErrorMessage(error);
            }
        },

        // Confirms and deletes the study set
        confirmDeleteSet() {
            if (confirm("Are you sure you want to delete this set?")) {
                this.deleteSet();
            }
        },

        // Deletes the study set and redirects
        async deleteSet() {
            try {
                await axiosAuthInstance.delete(`study_sets/study_sets/${this.setDetail.id}/`);
                this.$router.push('/my-study-sets/');
            } catch (error) {
                this.editSetError = extractFirstErrorMessage(error);
            }
        },

        // Toggles the form for creating a new term
        toggleCreateNewTerm() {
            this.creatingNewTerm = !this.creatingNewTerm;
            this.createTermError = null;
            this.resetNewTermForm();
        },

        // Resets the form for creating a new term
        resetNewTermForm() {
            this.newTerm = { front_text: '', back_text: '', study_set: this.setDetail.id };
        },

        // Creates a new term
        createTerm() {
            axiosAuthInstance.post('/study_sets/study_terms/', this.newTerm)
                .then(() => {
                    this.creatingNewTerm = false;
                    this.createTermError = null;
                    this.fetchSetDetail();
                })
                .catch(error => {
                    console.log(error.response ? error.response.data.message : 'Error fetching sets');
                });
        },

        // Enters edit mode for a specific term
        editTerm(term) {
            this.termForm = term && term.id ? { ...term } : null;
            this.editingTerm = term;
            this.editTermError = null;
        },

        // Updates the term
        async updateTerm() {
            if (this.editingTerm) {
                try {
                    await axiosAuthInstance.put(`/study_sets/study_terms/${this.editingTerm.id}/`, this.termForm);
                    this.editingTerm = null;
                    this.editTermError = null;
                    this.fetchSetDetail();
                } catch (error) {
                    this.editTermError = extractFirstErrorMessage(error);
                }
            }
        },

        // Confirms and deletes a term
        async confirmDeleteTerm(termId) {
            if (confirm("Are you sure you want to delete this term?")) {
                await this.deleteTerm(termId);
            }
        },

        // Deletes a term
        async deleteTerm(termId) {
            try {
                await axiosAuthInstance.delete(`study_sets/study_terms/${termId}/`);
                this.fetchSetDetail();
            } catch (error) {
                this.editTermError = extractFirstErrorMessage(error);
            }
        },
        // Toggle favorite/unfavorite for a study set
        toggleFavorite(set) {
            axiosAuthInstance.post(`/study_sets/favorite/${set.id}/`)
            .then(response => {
                set.favorited = response.data.status === 'favorited';
            })
            .catch(error => {
                console.error("Error toggling favorite status:", error.response ? error.response.data : error);
            });
        },
        speak(text) {
            if (!window.speechSynthesis) {
                alert("Text-to-speech not supported in this browser.");
                return;
            }

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.lang = 'ja-JP'; //TODO make variable
            window.speechSynthesis.speak(utterance);
        },
    }
};
</script>


<style scoped>
.set-banner {
    position: relative;
    background-color: #f0f0f0;
    padding: 1rem;
    border-radius: 0.4rem;
}

.set-banner > button {
    position: absolute;
    top: 1rem;
    right: 1rem;
}

.set-banner .favorite-btn {
    left: 1rem !important;
    margin-right: 1rem;
    font-size: 1.2rem;
    color: var(--clr-btn-yellow) !important;
    background-color: inherit !important;
}

.set-banner h1 {
    padding: 1rem 4rem 0 4rem;
}

.set-banner p {
    padding: 0.4rem 3rem 1rem 3rem;
}

.set-banner-edit {
    display: flex;
    flex-direction: row;
}

.set-banner-edit div:nth-child(1) {
    flex-grow: 1;
}

.set-banner input {
    padding-right: 4rem;
    height: 3rem;
    width: 100%;
}

.set-banner textarea {
    padding-right: 4rem;
    height: 6rem;
    width: 100%;
    min-width: 100%;
    max-width: 100%;
}

.set-banner select {
    padding-right: 4rem;
    width: 100%;
}

.set-banner input, .set-banner textarea {
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

/* Terms Display */

.terms-list {
    margin: 0 1rem 0 1rem;
}

.study-terms {
    margin-bottom: 20px;
}

.study-terms h2 {
    margin-bottom: 15px;
}

.term-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    background-color: #f8f8f8;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}

.term-display {
    display: flex;
    flex-direction: row;
    justify-content: center;
    width: 100%;
}

.front-back-display {
    display: flex;
    justify-content: center;
    width: 100%;
}

.front-back-display span {
    display: flex;
    cursor: pointer;
    padding: 0.6rem 1rem 0.6rem 1rem;
    font-size: 1.2rem;
    gap: 0.5rem;
}

.front-back-display span:first-child {
    text-align: right;
}

.front-back-display span:last-child {
    text-align: left;
}

.spacer {
    flex-grow: 0;
    width: 0.2rem;
    border-radius: 0.33rem;
    background-color: gray;
}

/* Input and textarea styles for term inputs */

.new-term-form input {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.front-back-display textarea {
    height: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

</style>