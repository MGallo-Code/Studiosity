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
                <button type="button" @click="toggleEditingSet" class="square-btn yellow-btn"><font-awesome-icon
                        :icon="['fas', 'ban']" /></button>
                <button type="button" @click="confirmDeleteSet" class="square-btn red-btn"><font-awesome-icon
                        :icon="['fas', 'trash-alt']" /></button>
            </div>
        </form>
        <div class="set-banner" v-else>
            <button @click="toggleFavorite" class="favorite-btn square-btn"><font-awesome-icon
                    :icon="[setDetail.favorited ? 'fas' : 'far', 'star']" /></button>
            <button @click="toggleEditingSet" class="square-btn blue-btn"><font-awesome-icon
                    :icon="['fas', 'edit']" /></button>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </div>

        <!-- Study Terms List -->
        <div class="terms-list">
            <!-- Inline form for creating a new term -->
            <div v-if="creatingNewTerm" class="term-container">
                <p v-if="createTermError" class="error-message">{{ createTermError }}</p>
                <form class="term-display" @submit.prevent="createNewTerm">
                    <div class="front-back-display">
                        <div class="img-info-flow">
                            <input type="file" @change="onCreateFrontImageSelected" />
                            <span>
                                <textarea v-model="createNewTermForm.front_text" />
                                <p @click="speak(createNewTermForm.front_text)"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                        <div class="spacer"></div>
                        <div class="img-info-flow">
                            <input type="file" @change="onCreateBackImageSelected" />
                            <span>
                                <textarea v-model="createNewTermForm.back_text" />
                                <p @click="speak(createNewTermForm.back_text)"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                    </div>
                    <div class="btn-stack">
                        <button type="submit" class="square-btn green-btn"><font-awesome-icon
                                :icon="['fas', 'plus']" /></button>
                        <button type="button" @click="toggleCreatingTerm" class="square-btn yellow-btn"><font-awesome-icon
                                :icon="['fas', 'ban']" /></button>
                    </div>
                </form>
            </div>

            <!-- Button to toggle new term creation form -->
            <button @click="toggleCreatingTerm" :disabled="creatingNewTerm">Create New Term</button>

            <!-- Iterating over each term to display -->
            <div v-for="term in studyTerms" :key="term.id" class="term-container">
                <!-- Editable term form -->
                <p v-if="editTermError && termEditForm && termEditForm.id === term.id" class="error-message">{{
                    editTermError }}</p>
                <form v-if="termEditForm && termEditForm.id === term.id" class="term-display" @submit.prevent="updateTerm">
                    <div class="front-back-display">
                        <div class="img-info-flow">
                            <picture v-if="term.front_image">
                                <img :src="term.front_image.file_path" />
                                <button type="button" @click="confirmDeleteTermImage('front_image')"
                                    class="square-btn red-btn">X</button>
                            </picture>
                            <input v-if="!term.front_image" type="file" @change="onUpdateFrontImageSelected" />
                            <span>
                                <textarea v-model="termEditForm.front_text" />
                                <p @click="speak(termEditForm.front_text)"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                        <div class="spacer"></div>
                        <div class="img-info-flow">
                            <picture v-if="term.back_image">
                                <img :src="term.back_image.file_path" />
                                <button type="button" @click="confirmDeleteTermImage('back_image')"
                                    class="square-btn red-btn">X</button>
                            </picture>
                            <input v-if="!term.back_image" type="file" @change="onUpdateBackImageSelected" />
                            <span>
                                <textarea v-model="termEditForm.back_text" />
                                <p @click="speak(termEditForm.back_text)"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                    </div>
                    <div class="btn-stack">
                        <button type="submit" class="square-btn green-btn"><font-awesome-icon
                                :icon="['fas', 'check']" /></button>
                        <button type="button" @click="toggleEditingTerm(null)"
                            class="square-btn yellow-btn"><font-awesome-icon :icon="['fas', 'ban']" /></button>
                        <button type="button" @click="confirmDeleteTerm(term.id)"
                            class="square-btn red-btn"><font-awesome-icon :icon="['fas', 'trash-alt']" /></button>
                    </div>
                </form>
                <!-- Display term details -->
                <div v-else class="term-display">
                    <div class="front-back-display">
                        <div class="img-info-flow">
                            <picture v-if="term.front_image">
                                <img :src="term.front_image.file_path" />
                            </picture>
                            <span @click="speak(term.front_text)">
                                <p>{{ term.front_text }}</p>
                                <p v-if="term.front_text != ''"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                        <div class="spacer"></div>
                        <div class="img-info-flow">
                            <picture v-if="term.back_image">
                                <img :src="term.back_image.file_path" />
                            </picture>
                            <span @click="speak(term.back_text)">
                                <p>{{ term.back_text }}</p>
                                <p v-if="term.back_text != ''"><font-awesome-icon icon="volume-up" /></p>
                            </span>
                        </div>
                    </div>
                    <button @click="toggleEditingTerm(term)" class="square-btn blue-btn"><font-awesome-icon
                            :icon="['fas', 'edit']" /></button>
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
        // Fetch initial data when component is created
        this.fetchSetDetail();
        this.fetchSetTerms();
    },
    methods: {
        // Fetches details of the study set
        async fetchSetDetail() {
            try {
                const setId = this.$route.params.id;
                const setResponse = await axiosAuthInstance.get(`study_sets/study_sets/${setId}/`);
                this.setDetail = setResponse.data;
            } catch (error) {
                // If set not found (no permission)
                if (error.response && error.response.data.detail === "Not found.") {
                    this.$router.push({ path: '/my-study-sets/' })
                } else {
                    console.log(error.response ? error.response.data.message : 'Error fetching sets');
                }
            }
        },
        // Fetches study terms for set
        async fetchSetTerms() {
            try {
                const setId = this.$route.params.id;
                const termsResponse = await axiosAuthInstance.get(`study_sets/terms_in_set/${setId}/`);
                this.studyTerms = termsResponse.data;
            } catch (error) {
                // If set not found (no permission)
                if (error.response && error.response.data.detail === "Not found.") {
                    this.$router.push({ path: '/my-study-sets/' })
                } else {
                    console.log(error.response ? error.response.data.message : 'Error fetching terms');
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
                    study_set: this.setDetail.id
                };
            }
            this.creatingNewTerm = !this.creatingNewTerm;
            this.createTermError = null;
        },
        // Creates a new term
        async createNewTerm() {
            // Create new term
            this.createTermError = null;
            try {
                const createTermResponse = await axiosAuthInstance.post('/study_sets/study_terms/', {
                    front_text: this.createNewTermForm.front_text,
                    back_text: this.createNewTermForm.back_text,
                    study_set: this.setDetail.id,
                });

                const imgUploadError = await this.updateTermImages(createTermResponse.data.id, this.createNewTermForm);

                // Toggle creation view
                this.toggleCreatingTerm();
                // Enter set edit mode if image upload(s) fail
                if (imgUploadError) {
                    this.this.fetchSetTerms();
                    this.toggleEditingTerm(createTermResponse.data)
                    this.editTermError = imgUploadError;
                    return;
                }
                this.fetchSetTerms();
            } catch (error) {
                this.createTermError = extractFirstErrorMessage(error);
            }
        },
        // Enters edit mode for a specific term (or exits if null provided as the term)
        toggleEditingTerm(term) {
            if (term) {
                this.termEditForm = { ...term };
                this.termEditForm.front_image = null;
                this.termEditForm.back_image = null;
            } else {
                this.termEditForm = null;
            }
            this.editTermError = null;
        },
        // Update selected image files
        onUpdateFrontImageSelected(event) {
            this.termEditForm.front_image = event.target.files[0];
        },
        onUpdateBackImageSelected(event) {
            this.termEditForm.back_image = event.target.files[0];
        },
        onCreateFrontImageSelected(event) {
            this.createNewTermForm.front_image = event.target.files[0];
        },
        onCreateBackImageSelected(event) {
            this.createNewTermForm.back_image = event.target.files[0];
        },
        // Updates the term
        async updateTerm() {
            try {
                const termUpdateBody = {
                    front_text: this.termEditForm.front_text,
                    back_text: this.termEditForm.back_text,
                }

                // Return early if image upload(s) fail
                const imgUploadError = await this.updateTermImages(this.termEditForm.id, this.termEditForm);
                if (imgUploadError) {
                    this.editTermError = imgUploadError;
                    return;
                }

                await axiosAuthInstance.patch(`/study_sets/study_terms/${this.termEditForm.id}/`, termUpdateBody);
                this.toggleEditingTerm(null);
                this.fetchSetTerms();
            } catch (error) {
                this.editTermError = extractFirstErrorMessage(error);
            }
        },
        async updateTermImages(studyTermId, imageForm) {
            try {
                const imageUploadForm = {
                    study_set: this.setDetail.id
                };
                // If new image files are selected, upload them
                if (imageForm.front_image) {
                    const formData = new FormData();
                    formData.append('file_path', imageForm.front_image);

                    const uploadImgResponse = await axiosAuthInstance.post('/uploads/images/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    });
                    imageUploadForm.front_image_id = uploadImgResponse.data.id;
                }
                if (imageForm.back_image) {
                    const formData = new FormData();
                    formData.append('file_path', imageForm.back_image);

                    const uploadImgResponse = await axiosAuthInstance.post('/uploads/images/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    });
                    imageUploadForm.back_image_id = uploadImgResponse.data.id;
                }
                if (!imageUploadForm.front_image_id && !imageUploadForm.back_image_id) {
                    return null;
                }
                await axiosAuthInstance.patch(`/study_sets/study_terms/${studyTermId}/`, imageUploadForm);
                // Return error status
                return null;
            } catch (error) {
                // Return error
                return extractFirstErrorMessage(error);
            }
        },
        // Confirms and deletes an image
        async confirmDeleteTermImage(imageField) {
            if (confirm("Are you sure you want to remove this image?")) {
                try {
                    const removeImageRequestBody = {}
                    removeImageRequestBody[imageField + '_id'] = null;

                    await axiosAuthInstance.patch(`/study_sets/study_terms/${this.termEditForm.id}/`, removeImageRequestBody);
                    this.fetchSetTerms();
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
                this.fetchSetTerms()
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
/* Main div holding set information/edit sections */
.set-banner {
    position: relative;
    width: 100%;
    background-color: #f0f0f0;
    padding: 1rem;
    border-radius: 8px;
}

/* Targets edit button in set-banner display */
.set-banner>button {
    position: absolute;
    top: 1rem;
    right: 1rem;
}

/* Targets favorite button in set-banner display, overrides rules above */
.set-banner .favorite-btn {
    left: 1rem !important;
    margin-right: 1rem;
    font-size: 1.2rem;
    color: var(--clr-btn-yellow) !important;
    background-color: inherit !important;
}

.set-banner .btn-stack {
    margin-left: 1rem;
}

/* Set title */
.set-banner h1 {
    padding: 1rem 4rem 0 4rem;
}

/* Set description */
.set-banner p {
    padding: 0.4rem 3rem 1rem 3rem;
}

/* Set banner edit form, contains:
    - div : .set-edit-fields
    - div : .btn-stack
*/
form.set-banner {
    display: flex;
    flex-direction: row;
    align-items: normal;
}

/* Div containing inputs for set updates */
form.set-banner .set-edit-fields {
    flex-grow: 1;
}

/* Set title input */
.set-banner input {
    margin-bottom: 0.6rem;
    padding: 0.5rem 4rem 0.5rem 0.5rem;
    height: 3rem;
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Set description input */
.set-banner textarea {
    margin-bottom: 0.6rem;
    padding: 0.5rem 4rem 0.5rem 0.5rem;
    height: 6rem;
    width: 100%;
    resize: none;
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Set privacy input */
.set-banner select {
    padding-right: 4rem;
    width: 100%;
}


/* TERMS CSS OPTIONS */


/* Outermost Terms list container */
.terms-list {
    margin: 0 1rem 0 1rem;
}

/* Level 1 term container, contains:
    - div/form : .term-display
    - div : .btn-stack
*/
.term-container {
    display: flex;
    gap: 1rem;
    flex-direction: column;
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #f8f8f8;
}

/* Level 2 term container, sets basic padding and contains:
    - div/form : .front-back-display
    - div : .btn-stack
*/
.term-display {
    display: flex;
    gap: 1rem;
    flex-direction: row;
    padding: 1rem;
    width: 100%;
}

/* Level 3 term container, the non-btn-stack half with display/inputs.
    Contains:
        - span : .front-back-display span
            (display front card info)
        - div : .spacer
        - span : .front-back-display span
            (display back card info)
*/
.front-back-display {
    flex: 1 1 auto;
    display: flex;
    gap: 0.6rem;
    flex-direction: row;
    /* Ensure maximum width stays below .btn-stack's position */
    max-width: calc(100%-5rem);
}

/* Level 4 term container, separates text from image */
.img-info-flow {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    max-width: 100%;
    overflow: hidden;
    align-items: center;
}

/* Level 5 term container, organizes front/back info displays */
.front-back-display span {
    display: flex;
    gap: 0.4rem;
    justify-content: center;
    cursor: pointer;
}

/* Level 5 term container, ONLY in display format */
:not(form)>.front-back-display span {
    padding-top: 0.8rem;
    padding-bottom: 0.8rem;
}

/* Term image selectors */
.front-back-display>input,

/* Term images */
.front-back-display picture {
    position: relative;
    max-width: 100%;
    width: 12rem;
    height: 12rem;
}

.front-back-display img {
    width: 100%;
    height: 100%;
    overflow: hidden;
    object-fit: cover;
    border-radius: 12px;
    border: 2px solid var(--clr-base-primary);
}

/* Button to remove images */
.front-back-display picture button {
    position: absolute;
    left: 0.5rem;
    top: 0.5rem;
    border-radius: 12px !important;
    border: 2px solid white;
}

.front-back-display picture button:hover {
    opacity: 1 !important;
    background-color: rgb(248, 84, 84);
    border: 2px solid rgb(250, 100, 100);
}

/* Term front/back textarea input */
.front-back-display textarea {
    width: 100%;
    resize: vertical;
}

/* Small spacer between front/back term information */
.spacer {
    flex: 0 0 auto;
    width: 0.2rem;
    border-radius: 8px;
    background-color: var(--clr-base-primary);
}
</style>