<template>
    <div class="set-detail-container">
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <!-- Editable Study Set Details -->
        <div class="set-banner" v-if="editingSet">
            <input type="text" v-model="setDetail.title" />
            <textarea v-model="setDetail.description"></textarea>
            <button @click="updateSetDetails">✔</button>
            <button @click="confirmDeleteSet">Delete Set</button>
        </div>
        <div class="set-banner" v-else>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
            <button @click="editSetDetails">✏️</button>
        </div>

        <!-- Study Terms List -->
        <div class="study-terms">
            <h2>Study Terms</h2>
            <!-- Inline form to create a new term -->
            <div class="term-item new-term-form" v-if="creatingNewTerm">
                <input type="text" placeholder="Front text" v-model="newTerm.front_text" />
                <input type="text" placeholder="Back text" v-model="newTerm.back_text" />
                <button @click="createTerm">Create</button>
            </div>

            <button @click="toggleCreateNewTerm">Create New Term</button>

            <div v-for="term in studyTerms" :key="term.id" class="term-item">
                <div v-if="editingTerm && editingTerm.id === term.id">
                    <!-- Edit form for the term -->
                    <input type="text" v-model="termForm.front_text" />
                    <input type="text" v-model="termForm.back_text" />
                    <button @click="updateTerm">✔️ Save</button>
                    <button @click="confirmDeleteTerm(term.id)">Delete</button>
                </div>
                <div v-else>
                    <!-- Display term details -->
                    <div><strong>Front:</strong> {{ term.front_text }}</div>
                    <div><strong>Back:</strong> {{ term.back_text }}</div>
                    <button @click="editTerm(term)">Edit</button>
                    <!-- Delete button is not shown here -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { axiosAuthInstance } from '../utils/axios-config';

export default {
    data() {
        return {
            setDetail: {},
            studyTerms: [],
            error: null,
            editingSet: false,
            editingTerm: null,
            editingTermId: null,
            showModal: false,
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
        this.fetchSetDetail();
    },
    methods: {
        async fetchSetDetail() {
            try {
                const setId = this.$route.params.id;
                this.termForm.study_set = setId; // Linking the term to the set
                const setResponse = await axiosAuthInstance.get(`study_sets/study_sets/${setId}/`);
                this.setDetail = setResponse.data;

                const termsResponse = await axiosAuthInstance.get(`study_sets/terms_in_set/${setId}/`);
                this.studyTerms = termsResponse.data;
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred';
            }
        },

        editSetDetails() {
            this.editingSet = true;
        },

        async updateSetDetails() {
            try {
                await axiosAuthInstance.put(`/study_sets/study_sets/${this.setDetail.id}/`, this.setDetail);
                this.editingSet = false;
                // Refresh set details
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'Error updating set details';
            }
        },

        confirmDeleteSet() {
            if (confirm("Are you sure you want to delete this set?")) {
                this.deleteSet();
            }
        },
        async deleteSet() {
            try {
                await axiosAuthInstance.delete(`study_sets/study_sets/${this.setDetail.id}/`);
                this.$router.push('/my-study-sets/'); // Redirect after deletion
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'Error deleting set';
            }
        },

        toggleCreateNewTerm() {
            this.creatingNewTerm = !this.creatingNewTerm;
            this.resetNewTermForm();
            if (this.creatingNewTerm) {
                this.newTerm.study_set = this.setDetail.id;
            }
        },
        resetNewTermForm() {
            this.newTerm = { front_text: '', back_text: '', study_set: this.setDetail.id };
        },
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

        createNewTerm() {
            this.editingTermId = null;
            this.termForm = { front_text: '', back_text: '', study_set: this.setDetail.id };
            this.showModal = true;
        },

        editTerm(term) {
            // Check if we are already in editing mode for this term
            if (this.editingTerm && this.editingTerm.id === term.id) {
                // If we are, turn off editing mode
                this.editingTerm = null;
            } else {
                // Otherwise, enter editing mode for this term
                this.editingTerm = term;
                this.termForm = { ...term };
            }
        },

        async updateTerm() {
            try {
                if (this.editingTerm) {
                    await axiosAuthInstance.put(`/study_sets/study_terms/${this.editingTerm.id}/`, this.termForm);
                    // Turn off editing mode
                    this.editingTerm = null;
                    this.fetchSetDetail();
                }
            } catch (error) {
                this.error = error.response ? error.response.data.detail : "An error occurred while updating the term.";
            }
        },

        async submitTermForm() {
            try {
                if (this.editingTermId) {
                    await axiosAuthInstance.put(`/study_sets/study_terms/${this.editingTermId}/`, this.termForm);
                } else {
                    await axiosAuthInstance.post(`/study_sets/study_terms/`, this.termForm);
                }
                this.showModal = false;
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : "An error occurred while processing the term.";
            }
        },

        async confirmDeleteTerm(termId) {
            if (confirm("Are you sure you want to delete this term?")) {
                await this.deleteTerm(termId);
            }
        },

        async deleteTerm(termId) {
            try {
                await axiosAuthInstance.delete(`study_sets/study_terms/${termId}/`);
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while deleting the term';
            }
        },

        async duplicateTerm(term) {
            const newTerm = { ...term, id: undefined, study_set: this.termForm.study_set };
            try {
                await axiosAuthInstance.post(`study_sets/study_terms/`, newTerm);
                this.fetchSetDetail();
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while duplicating the term';
            }
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
}

.study-terms {
    margin-bottom: 20px;
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
}

.create-button:hover {
    opacity: 0.9;
}

.error-message {
    color: #f44336;
    text-align: center;
    margin-top: 10px;
}
</style>
