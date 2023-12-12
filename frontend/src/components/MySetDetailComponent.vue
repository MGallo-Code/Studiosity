<template>
    <!-- Container for the study set detail view -->
    <div class="set-detail-container">

        <!-- Error message display -->
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <!-- Editable Study Set Details -->
        <div class="set-banner" v-if="editingSet">
            <input type="text" v-model="setDetail.title" />
            <textarea v-model="setDetail.description"></textarea>
            <select v-model="setDetail.private">
                <option value="false">Public</option>
                <option value="true">Private</option>
            </select>
            <button @click="updateSetDetails">✔</button>
            <button @click="confirmDeleteSet"><font-awesome-icon icon="trash-alt" /></button>
        </div>
        <div class="set-banner" v-else>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
            <button @click="editSetDetails"><font-awesome-icon icon="edit" /></button>
        </div>

        <!-- Study Terms List -->
        <div class="study-terms">
            <h2>Study Terms</h2>

            <!-- Inline form for creating a new term -->
            <div class="term-item new-term-form" v-if="creatingNewTerm">
                <input type="text" placeholder="Front text" v-model="newTerm.front_text" />
                <input type="text" placeholder="Back text" v-model="newTerm.back_text" />
                <button @click="createTerm">Create</button>
            </div>

            <!-- Button to toggle new term creation form -->
            <button @click="toggleCreateNewTerm">Create New Term</button>

            <!-- Iterating over each term to display -->
            <div v-for="term in studyTerms" :key="term.id" class="term-item">
                <!-- Editable term form -->
                <div v-if="editingTerm && editingTerm.id === term.id">
                    <input type="text" v-model="termForm.front_text" />
                    <input type="text" v-model="termForm.back_text" />
                    <button @click="updateTerm">✔️ Save</button>
                    <button @click="confirmDeleteTerm(term.id)"><font-awesome-icon icon="trash-alt" /></button>
                </div>
                <!-- Display term details -->
                <div v-else>
                    <div><strong>Front:</strong> {{ term.front_text }}</div>
                    <div><strong>Back:</strong> {{ term.back_text }}</div>
                    <button @click="speak(term.front_text)"><font-awesome-icon icon="volume-up" /> Speak</button>
                    <button @click="duplicateTerm(term)"><font-awesome-icon icon="clone" /></button>
                    <button @click="editTerm(term)"><font-awesome-icon icon="edit" /></button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { axiosAuthInstance } from '../utils/axios-config';

export default {
    data() {
        // Initializing data properties
        return {
            setDetail: {},
            studyTerms: [],
            error: null,
            editingSet: false,
            editingTerm: null,
            editingTermId: null,
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
                    this.error = error.response ? error.response.data.detail : 'An error occurred';
                }
            }
        },

        // Toggles edit mode for the study set
        editSetDetails() {
            this.editingSet = true;
        },

        // Updates study set details
        async updateSetDetails() {
            try {
                await axiosAuthInstance.put(`/study_sets/study_sets/${this.setDetail.id}/`, this.setDetail);
                this.editingSet = false;
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'Error updating set details';
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
                this.error = error.response ? error.response.data.detail : 'Error deleting set';
            }
        },

        // Toggles the form for creating a new term
        toggleCreateNewTerm() {
            this.creatingNewTerm = !this.creatingNewTerm;
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
                    this.fetchSetDetail();
                })
                .catch(error => {
                    this.error = error.response ? error.response.data.detail : 'Error creating term';
                });
        },

        // Enters edit mode for a specific term
        editTerm(term) {
            this.editingTerm = this.editingTerm && this.editingTerm.id === term.id ? null : term;
            this.termForm = { ...term };
        },

        // Updates the term
        async updateTerm() {
            if (this.editingTerm) {
                try {
                    await axiosAuthInstance.put(`/study_sets/study_terms/${this.editingTerm.id}/`, this.termForm);
                    this.editingTerm = null;
                    this.fetchSetDetail();
                } catch (error) {
                    this.error = error.response ? error.response.data.detail : "An error occurred while updating the term.";
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
                this.error = error.response ? error.response.data.detail : 'An error occurred while deleting the term';
            }
        },

        // Duplicates a term
        async duplicateTerm(term) {
            const newTerm = { ...term, id: undefined };
            try {
                await axiosAuthInstance.post(`study_sets/study_terms/`, newTerm);
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while duplicating the term';
            }
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
.set-detail-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

.set-banner {
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
}

.set-banner h1 {
    margin-bottom: 10px;
}

.set-banner input, .set-banner textarea {
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.study-terms {
    margin-bottom: 20px;
}

.study-terms h2 {
    margin-bottom: 15px;
}

.term-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #f8f8f8;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}

.term-item button {
    margin-left: 10px;
    padding: 5px 10px;
    font-size: 0.9em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
}

.term-item button i {
    margin-right: 5px;
}

.term-item .edit-button {
    background-color: #4CAF50;
    color: white;
}

.term-item .delete-button {
    background-color: #f44336;
    color: white;
}

.term-item .duplicate-button {
    background-color: #2196F3;
    color: white;
}

.create-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    margin-top: 15px;
}

.create-button i {
    margin-right: 5px;
}

.create-button:hover {
    opacity: 0.9;
}

.error-message {
    color: #f44336;
    text-align: center;
    margin-top: 10px;
}

/* Input and textarea styles for new term form */
.new-term-form input, .new-term-form textarea {
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
    width: 100%;
}

.new-term-form button {
    background-color: #2196F3;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.new-term-form button:hover {
    opacity: 0.9;
}
</style>
