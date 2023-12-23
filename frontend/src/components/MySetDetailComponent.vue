<template>
    <main v-if="setDetail">
        <!-- Editable Study Set Details -->
        <form v-if="editingSet" class="set-banner" @submit.prevent="updateSetDetails">
            <div class="set-edit-fields">
                <p v-if="editSetError" class="error-message">{{ editSetError }}</p>
                <input type="text" v-model="setEditForm.title" />
                <textarea v-model="setEditForm.description"></textarea>
                <select v-model="setEditForm.private">
                    <option value="false">Public</option>
                    <option value="true">Private</option>
                </select>
            </div>
            <div class="btn-stack">
                <button type="submit" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'check']" /></button>
                <button type="button" @click="toggleEditingSet" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button>
                <button type="button" @click="confirmDeleteSet" class="square-btn red-btn"><font-awesome-icon :icon="['fas', 'trash-alt']" /></button>
            </div>
        </form>
        <div class="set-banner" v-else>
            <button @click="toggleFavorite" class="favorite-btn square-btn"><font-awesome-icon :icon="[setDetail.favorited ? 'fas' : 'far', 'star']" /></button>
            <button @click="toggleEditingSet" class="square-btn blue-btn"><font-awesome-icon :icon="['fas', 'edit']" /></button>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </div>

        <!-- Study Terms List -->
        <div class="terms-list">
            <!-- Inline form for creating a new term -->
            <form v-if="creatingNewTerm" class="term-container" @submit.prevent="createNewTerm">
                <p v-if="createTermError" class="error-message">{{ createTermError }}</p>
                <div class="term-display">
                    <div class="front-back-display">
                        <span>
                            <textarea v-model="createNewTermForm.front_text" />
                            <p @click="speak(createNewTermForm.front_text)"><font-awesome-icon icon="volume-up" /></p>
                        </span>
                        <div class="spacer"></div>
                        <span>
                            <textarea v-model="createNewTermForm.back_text" />
                            <p @click="speak(createNewTermForm.back_text)"><font-awesome-icon icon="volume-up" /></p>
                        </span> 
                    </div>
                    <div class="btn-stack">
                        <button type="submit" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'plus']" /></button>
                        <button type="button" @click="toggleCreatingTerm" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button> 
                    </div>
                </div>
            </form>

            <!-- Button to toggle new term creation form -->
            <button @click="toggleCreatingTerm" :disabled="creatingNewTerm">Create New Term</button>

            <!-- Iterating over each term to display -->
            <div v-for="term in studyTerms" :key="term.id" class="term-container">
                <!-- Editable term form -->
                <form v-if="termEditForm && termEditForm.id === term.id" class="term-display" @submit.prevent="updateTerm">
                    <p v-if="editTermError" class="error-message">{{ editTermError }}</p>
                    <div class="front-back-display">
                        <span>
                            <textarea v-model="termEditForm.front_text" />
                            <p @click="speak(termEditForm.front_text)"><font-awesome-icon icon="volume-up" /></p>
                        </span>
                        <div class="spacer"></div>
                        <span>
                            <textarea v-model="termEditForm.back_text" />
                            <p @click="speak(termEditForm.back_text)"><font-awesome-icon icon="volume-up" /></p>
                        </span>
                    </div>
                    <div class="btn-stack">
                        <button type="submit" class="square-btn green-btn"><font-awesome-icon :icon="['fas', 'check']" /></button>
                        <button type="button" @click="toggleEditingTerm(null)" class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button>
                        <button type="button" @click="confirmDeleteTerm(term.id)" class="square-btn red-btn"><font-awesome-icon :icon="['fas', 'trash-alt']" /></button>
                    </div>
                </form>
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
                    <button @click="toggleEditingTerm(term)" class="square-btn blue-btn"><font-awesome-icon :icon="['fas', 'edit']" /></button>
                </div>
            </div>
        </div>
    </main>
</template>


<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        return {
            // Loaded objects
            studyTerms: [],
            setDetail: null,
            // Errors
            editSetError: null,
            createTermError: null,
            editTermError: null,
            // Form state flags
            editingSet: false,
            creatingNewTerm: false,
            // Forms and errors
            setEditForm: null,
            termEditForm: null,
            createNewTermForm: null,
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
        // Toggle edit state for study set
        toggleEditingSet() {
            // Reset set edit form 
            if (!this.editingSet) {
                this.setEditForm = { ...this.setDetail };
            }
            this.editingSet = !this.editingSet;
            this.editSetError = null;
        },
        // Update set using setEditForm
        async updateSetDetails() {
            try {
                await axiosAuthInstance.put(`/study_sets/study_sets/${this.setDetail.id}/`, this.setEditForm);
                this.setDetail = { ...this.setEditForm };
                this.toggleEditingSet();
                this.fetchSetDetail();
            } catch (error) {
                this.editSetError = extractFirstErrorMessage(error);
            }
        },
        // Confirm and delete study set
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
        // Toggle favorite/unfavorite for study set
        toggleFavorite() {
            axiosAuthInstance.post(`/study_sets/favorite/${this.setDetail.id}/`)
            .then(response => {
                this.setDetail.favorited = response.data.status === 'favorited';
            })
            .catch(error => {
                console.error("Error toggling favorite status:", error.response ? error.response.data : error);
            });
        },

        // Toggles the form for creating a new term
        toggleCreatingTerm() {
            // Resets the form for creating a new term
            if (!this.creatingNewTerm) {
                this.createNewTermForm = {
                    front_text: '',
                    back_text: '',
                    front_image: null,
                    back_image: null,
                    study_set: this.setDetail.id};
            }
            this.creatingNewTerm = !this.creatingNewTerm;
            this.createTermError = null;
        },
        // Creates a new term
        createNewTerm() {
            axiosAuthInstance.post('/study_sets/study_terms/', this.createNewTermForm)
                .then(() => {
                    this.toggleCreatingTerm()
                    this.fetchSetDetail();
                })
                .catch(error => {
                    console.log(error.response ? error.response.data.message : 'Error creating new term');
                });
        },

        // Enters edit mode for a specific term (or exits if null provided as the term)
        toggleEditingTerm(term) {
            this.termEditForm = term ? { ...term } : null;
            this.editTermError = null;
        },
        // Updates the term
        async updateTerm() {
            try {
                await axiosAuthInstance.put(`/study_sets/study_terms/${this.termEditForm.id}/`, this.termEditForm);
                this.toggleEditingTerm(null);
                this.fetchSetDetail();
            } catch (error) {
                this.editTermError = extractFirstErrorMessage(error);
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
    width: 100%;
    background-color: #f0f0f0;
    padding: 1rem;
    border-radius: 0.4rem;
}

/* Targets the edit button in set-banner display */
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

form.set-banner {
    display: flex;
    flex-direction: row;
    align-items: normal;
}

form.set-banner .set-edit-fields {
    flex-grow: 1;
}

.set-banner input {
    margin-bottom: 0.6rem;
    padding: 0.5rem 4rem 0.5rem 0.5rem;
    height: 3rem;
    width: 100%;
    border-radius: 0.4rem;
    border: 1px solid #ddd;
}

.set-banner textarea {
    margin-bottom: 0.6rem;
    padding: 0.5rem 4rem 0.5rem 0.5rem;
    height: 6rem;
    width: 100%;
    resize: none;
    border-radius: 0.4rem;
    border: 1px solid #ddd;
}

.set-banner select {
    padding-right: 4rem;
    width: 100%;
}

/* Terms Display */

.terms-list {
    margin: 0 1rem 0 1rem;
}

.term-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin: 0;
    padding: 1rem;
    width: 100%;
    border-radius: 0.4rem;
    border: 1px solid #ddd;
    background-color: #f8f8f8;
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

form.term-container input {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

form.term-container textarea {
    height: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

</style>