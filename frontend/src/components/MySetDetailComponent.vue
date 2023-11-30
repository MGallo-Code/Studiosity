<template>
    <div class="set-detail-container">
        <div v-if="error" class="error-message">{{ error }}</div>
        <div class="set-banner">
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </div>

        <div class="study-terms">
            <h2>Study Terms</h2>
            <button class="create-button" @click="createNewTerm">Create New Term</button>
            <div v-for="term in studyTerms" :key="term.id" class="term-item">
                <div>
                    <strong>Front:</strong> {{ term.front_text }}
                </div>
                <div>
                    <strong>Back:</strong> {{ term.back_text }}
                </div>
                <button class="edit-button" @click="editTerm(term)">Edit</button>
                <button class="delete-button" @click="confirmDeleteTerm(term.id)">Delete</button>
                <button class="duplicate-button" @click="duplicateTerm(term)">Duplicate</button>
            </div>
        </div>

        <ModalComponent :showModal="showModal" @update:showModal="showModal = $event">
            <form @submit.prevent="submitForm">
                <div v-if="modalError" class="error-message">{{ modalError }}</div>
                <label for="front_text">Front Text:</label>
                <input type="text" id="front_text" v-model="termForm.front_text" required>
                
                <label for="back_text">Back Text:</label>
                <input type="text" id="back_text" v-model="termForm.back_text" required>
                
                <!-- Include other inputs for additional term attributes here -->

                <div class="modal-footer">
                    <button type="button" @click="toggleModal">Cancel</button>
                    <button type="submit">{{ isEditMode ? 'Update Term' : 'Create Term' }}</button>
                </div>
            </form>
        </ModalComponent>
    </div>
</template>

<script>
import ModalComponent from './ModalComponent.vue'; // Adjust path as necessary
import { axiosAuthInstance } from '../utils/axios-config';

export default {
    components: {
        ModalComponent
    },
    data() {
        return {
            setDetail: {},
            studyTerms: [],
            error: null,
            modalError: null,
            showModal: false,
            isEditMode: false,
            editingTermId: null,
            termForm: {
                study_set: null,
                front_text: '',
                back_text: '',
                // Include other term attributes here
            }
        };
    },
    created() {
        this.fetchSetDetail();
    },
    methods: {
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
        editTerm(term) {
            this.isEditMode = true;
            this.editingTermId = term.id;
            this.termForm = {
                study_set: this.termForm.study_set,
                ...term
            };
            this.showModal = true;
        },
        async confirmDeleteTerm(termId) {
            if (confirm("Are you sure you want to delete this term?")) {
                await this.deleteTerm(termId);
            }
        },
        async deleteTerm(termId) {
            try {
                await axiosAuthInstance.delete(`study_sets/study_terms/${termId}/`);
                this.fetchSetDetail(); // Refresh the list after deletion
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while deleting the term';
            }
        },
        async duplicateTerm(term) {
            const newTerm = {
                // Copy the fields you need from the term to duplicate
                study_set: this.termForm.study_set,
                front_text: term.front_text,
                back_text: term.back_text,
                // Add other fields if necessary
            };
            try {
                await axiosAuthInstance.post(`study_sets/study_terms/`, newTerm);
                this.fetchSetDetail(); // Refresh the list after duplication
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while duplicating the term';
            }
        },
        createNewTerm() {
            this.isEditMode = false;
            this.editingTermId = null;
            this.termForm = {
                study_set: this.termForm.study_set,
                front_text: '',
                back_text: '',
                // Reset other term attributes
            };
            this.showModal = true;
        },
        async submitForm() {
            this.modalError = null;
            if (this.termForm.front_text == '' || this.termForm.back_text == '') {
                this.modalError = "Please fill in both sides of the term!";
                return;
            }
            try {
                if (this.isEditMode) {
                    await axiosAuthInstance.put(`study_sets/study_terms/${this.editingTermId}/`, this.termForm);
                } else {
                    await axiosAuthInstance.post(`study_sets/study_terms/`, this.termForm);
                }
                this.toggleModal();
                this.fetchSetDetail();
            } catch (error) {
                this.modalError = error.response ? error.response.data.detail : "An error occurred while processing the term.";
            }
        },
        toggleModal() {
            this.showModal = !this.showModal;
            if (!this.showModal) {
                this.resetForm();
            }
        },
        resetForm() {
            this.isEditMode = false;
            this.editingTermId = null;
            this.termForm = {
                study_set: this.termForm.study_set,
                front_text: '',
                back_text: '',
                // Reset other term attributes
            };
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
