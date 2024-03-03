<template>
    <main v-if="setDetail">
        <section id="page-topper">
            <span>Viewing My Set: {{ setDetail.title }}</span>
        </section>
        <!-- Editable Study Set Details -->
        <form v-if="isEditingSet" class="main-header set-banner" @submit.prevent="updateSetDetails">
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
                <button type="submit" class="square-btn green-btn"><font-awesome-icon class="fa-icon"
                        :icon="['fas', 'check']" /></button>
                <button type="button" @click="toggleEditingSet" class="square-btn yellow-btn"><font-awesome-icon
                        class="fa-icon" :icon="['fas', 'ban']" /></button>
                <button type="button" @click="confirmDeleteSet" class="square-btn red-btn"><font-awesome-icon
                        class="fa-icon" :icon="['fas', 'trash-alt']" /></button>
            </div>
        </form>
        <div class="main-header set-banner" v-else>
            <button @click="toggleFavorite" class="square-btn favorite-btn transparent-btn"><font-awesome-icon class="fa-icon"
                    :icon="[setDetail.favorited ? 'fas' : 'far', 'star']" /></button>
            <button @click="toggleEditingSet" class="square-btn transparent-btn"><font-awesome-icon class="fa-icon"
                    :icon="['fas', 'edit']" /></button>
            <h1>{{ setDetail.title }}</h1>
            <p>{{ setDetail.description || 'No description provided.' }}</p>
        </div>


        <!-- Inline form for creating a new term -->
        <div v-if="isCreatingNewTerm" class="term-container" id="create-term-form">
            <p v-if="createTermError" class="error-message">{{ createTermError }}</p>
            <form class="term-display" @submit.prevent="createNewTerm">
                <div class="term-info-display">
                    <div class="img-info-flow">
                        <input type="file" @change="onCreateFrontImageSelected" />
                        <span>
                            <textarea v-model="termCreateForm.front_text" />
                            <p @click="speak(termCreateForm.front_text)"></p>
                        </span>
                        <span>
                            <!-- Front Language Selection -->
                            <select v-model="termCreateForm.selectedFrontLanguage"
                                @change="() => updateVoiceOptions(termCreateForm, 'Front')">
                                <option v-for="language in availableLanguages" :key="language" :value="language">
                                    {{ language }}
                                </option>
                            </select>
                            <!-- Front Voice ID Selection -->
                            <select v-model="termCreateForm.selectedFrontVoiceId">
                                <option v-for="voice in termCreateForm.filteredFrontVoices" :key="voice.Id"
                                    :value="voice.Id">
                                    {{ voice.Name }}
                                </option>
                            </select>
                        </span>
                    </div>
                    <div class="img-info-flow">
                        <input type="file" @change="onCreateBackImageSelected" />
                        <span>
                            <textarea v-model="termCreateForm.back_text" />
                            <p @click="speak(termCreateForm.back_text)"></p>
                        </span>
                        <span>
                            <!-- Back Language Selection -->
                            <select v-model="termCreateForm.selectedBackLanguage"
                                @change="() => updateVoiceOptions(termCreateForm, 'Back')">
                                <option v-for="language in availableLanguages" :key="language" :value="language">
                                    {{ language }}
                                </option>
                            </select>
                            <!-- Back Voice ID Selection -->
                            <select v-model="termCreateForm.selectedBackVoiceId">
                                <option v-for="voice in termCreateForm.filteredBackVoices" :key="voice.Id"
                                    :value="voice.Id">
                                    {{ voice.Name }}
                                </option>
                            </select>
                        </span>
                    </div>
                </div>
                <div class="btn-stack">
                    <button type="submit" class="square-btn green-btn"><font-awesome-icon class="fa-icon"
                            :icon="['fas', 'plus']" /></button>
                    <button type="button" @click="toggleCreatingTerm" class="square-btn yellow-btn"><font-awesome-icon
                            class="fa-icon" :icon="['fas', 'ban']" /></button>
                </div>
            </form>
        </div>

        <!-- Button to toggle new term creation form -->
        <div class="control-bar term-btn-menu">
            <button @click="toggleCreatingTerm" :disabled="isCreatingNewTerm || isChangingOrder">Create New Term</button>
            <button @click="toggleChangingOrder"
                :disabled="isTogglingChangeOrderMode || !studyTerms || studyTerms.length == 0">
                {{ isChangingOrder ? "Save Term Order" : "Edit Term Order" }}</button>
        </div>

        <Sortable v-if="isChangingOrder" class="terms-list" :list="studyTerms" :itemKey="id" options="options">
            <template #item="{ element }">
                <div class="draggable term-container" :id="`studyTermId=${element.id}`" :key="element.id">
                    <div class="term-display term-display-reorder">
                        <div class="term-info-display">
                            <div class="img-info-flow">
                                <picture v-if="element.front_image">
                                    <img :src="element.front_image.file_path" />
                                </picture>
                                <span>
                                    <p>{{ element.front_text }}</p>
                                </span>
                            </div>
                            <div class="img-info-flow">
                                <picture v-if="element.back_image">
                                    <img :src="element.back_image.file_path" />
                                </picture>
                                <span>
                                    <p>{{ element.back_text }}</p>
                                </span>
                            </div>
                        </div>
                        <font-awesome-icon :icon="['fas', 'sort']" class="fa-icon reorder-symbol" />
                    </div>
                </div>
            </template>
        </Sortable>

        <section v-else class="terms-list">
            <!-- Iterating over each term to display -->
            <div v-for="term in studyTerms" :key="term.id" class="term-container">
                <!-- Editable term form -->
                <p v-if="editTermError && termEditForm && termEditForm.id === term.id" class="error-message">{{
                    editTermError }}</p>
                <form v-if="termEditForm && termEditForm.id === term.id" class="term-display" @submit.prevent="updateTerm">
                    <div class="term-info-display">
                        <div class="img-info-flow">
                            <picture v-if="term.front_image">
                                <img :src="term.front_image.file_path" />
                                <button type="button" @click="confirmDeleteTermImage('front_image')"
                                    class="square-btn red-btn">X</button>
                            </picture>
                            <input v-if="!term.front_image" type="file" @change="onUpdateFrontImageSelected" />
                            <span>
                                <textarea v-model="termEditForm.front_text" />
                            </span>
                            <span>
                                <!-- Front Language Selection -->
                                <select v-model="termEditForm.selectedFrontLanguage"
                                    @change="() => updateVoiceOptions(termEditForm, 'Front')">
                                    <option v-for="language in availableLanguages" :key="language" :value="language">
                                        {{ language }}
                                    </option>
                                </select>
                                <!-- Front Voice ID Selection -->
                                <select v-model="termEditForm.selectedFrontVoiceId">
                                    <option v-for="voice in termEditForm.filteredFrontVoices" :key="voice.Id"
                                        :value="voice.Id">
                                        {{ voice.Name }}
                                    </option>
                                </select>
                            </span>
                        </div>
                        <div class="img-info-flow">
                            <picture v-if="term.back_image">
                                <img :src="term.back_image.file_path" />
                                <button type="button" @click="confirmDeleteTermImage('back_image')"
                                    class="square-btn red-btn">X</button>
                            </picture>
                            <input v-if="!term.back_image" type="file" @change="onUpdateBackImageSelected" />
                            <span>
                                <textarea v-model="termEditForm.back_text" />
                            </span>
                            <span>
                                <!-- Back Language Selection -->
                                <select v-model="termEditForm.selectedBackLanguage"
                                    @change="() => updateVoiceOptions(termEditForm, 'Back')">
                                    <option v-for="language in availableLanguages" :key="language" :value="language">
                                        {{ language }}
                                    </option>
                                </select>
                                <!-- Back Voice ID Selection -->
                                <select v-model="termEditForm.selectedBackVoiceId">
                                    <option v-for="voice in termEditForm.filteredBackVoices" :key="voice.Id"
                                        :value="voice.Id">
                                        {{ voice.Name }}
                                    </option>
                                </select>
                            </span>
                        </div>
                    </div>
                    <div class="btn-stack">
                        <button type="submit" class="square-btn green-btn"><font-awesome-icon class="fa-icon"
                                :icon="['fas', 'check']" /></button>
                        <button type="button" @click="toggleEditingTerm(null)"
                            class="square-btn yellow-btn"><font-awesome-icon class="fa-icon"
                                :icon="['fas', 'ban']" /></button>
                        <button type="button" @click="confirmDeleteTerm(term.id)"
                            class="square-btn red-btn"><font-awesome-icon class="fa-icon"
                                :icon="['fas', 'trash-alt']" /></button>
                    </div>
                </form>
                <!-- Display term details -->
                <div v-else class="term-display">
                    <div class="term-info-display">
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
                    <button @click="toggleEditingTerm(term)" class="square-btn transparent-btn"><font-awesome-icon
                            class="fa-icon" :icon="['fas', 'edit']" /></button>
                </div>
            </div>
        </section>
    </main>
</template>


<script setup>
import { Sortable } from "sortablejs-vue3";
</script>
<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        return {
            // Loaded objects
            studyTerms: [],
            studyTermOrders: null,
            setDetail: null,
            // AWS Polly voices
            availableVoices: null,
            availableLanguages: null,
            // Errors
            editSetError: null,
            createTermError: null,
            editTermError: null,
            // Form state flags
            isChangingOrder: false,
            isTogglingChangeOrderMode: false,
            isTogglingCreateTerm: false,
            isEditingSet: false,
            isCreatingNewTerm: false,
            // Forms
            setEditForm: null,
            termEditForm: null,
            termCreateForm: null,
        };
    },
    created() {
        // Fetch initial data when component is created
        this.fetchSetDetail();
        this.fetchSetTerms();
    },
    methods: {
        // { API FETCHING }

        // Fetches details of the study set
        async fetchSetDetail() {
            try {
                const setId = this.$route.params.id;
                const setResponse = await axiosAuthInstance.get(`study_sets/${setId}/`);
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
                const termsResponse = await axiosAuthInstance.get(`study_sets/${setId}/terms/`);
                // Sort our response by sort_order
                const terms = termsResponse.data;
                terms.sort((a, b) => a.sort_order - b.sort_order);
                this.studyTerms = terms;
            } catch (error) {
                // If set not found (no permission)
                if (error.response && error.response.data.detail === "Not found.") {
                    this.$router.push({ path: '/my-study-sets/' })
                } else {
                    console.log(error.response ? error.response.data.message : 'Error fetching terms');
                }
            }
        },
        async fetchPollyVoices() {
            try {
                const response = await axiosAuthInstance.get('/study_sets/get_voices/');
                this.availableVoices = response.data.voices;
                // Process voices as needed, e.g., extract languages
                this.processVoices();
            } catch (error) {
                console.log(error.response ? error.response.data.message : 'Error fetching polly voices');
            }
        },
        processVoices() {
            // Extract unique languages from the voices
            this.availableLanguages = [...new Set(this.availableVoices.map(voice => voice.LanguageName))];
            this.availableLanguages.sort();
        },


        // MANAGING SET

        // Toggle edit state for study set
        toggleEditingSet() {
            // Reset set edit form 
            if (!this.isEditingSet) {
                this.setEditForm = { ...this.setDetail };
            }
            this.isEditingSet = !this.isEditingSet;
            this.editSetError = null;
        },
        // Update set using setEditForm
        async updateSetDetails() {
            try {
                await axiosAuthInstance.put(`/study_sets/${this.setDetail.id}/`, this.setEditForm);
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
                await axiosAuthInstance.delete(`study_sets/${this.setDetail.id}/`);
                this.$router.push('/my-study-sets/');
            } catch (error) {
                this.editSetError = extractFirstErrorMessage(error);
            }
        },


        // { FAVORITING SET }

        // Toggle favorite/unfavorite for study set
        toggleFavorite() {
            axiosAuthInstance.post(`/study_sets/${this.setDetail.id}/favorite/`)
                .then(response => {
                    this.setDetail.favorited = response.data.status === 'favorited';
                })
                .catch(error => {
                    console.error("Error toggling favorite status:", error.response ? error.response.data : error);
                });
        },


        // { LANGUAGE/VOICE SELECTION }

        // Select the language filter based on selected voice
        initializeVoiceSelections(form, term) {
            if (term.front_voice_id) {
                const frontVoice = this.availableVoices.find(voice => voice.Id === term.front_voice_id);
                if (frontVoice) {
                    form.selectedFrontLanguage = frontVoice.LanguageName;
                    form.selectedFrontVoiceId = term.front_voice_id;
                    this.updateFilteredVoices(form, 'Front');
                }
            }
            if (term.back_voice_id) {
                const backVoice = this.availableVoices.find(voice => voice.Id === term.back_voice_id);
                if (backVoice) {
                    form.selectedBackLanguage = backVoice.LanguageName;
                    form.selectedBackVoiceId = term.back_voice_id;
                    this.updateFilteredVoices(form, 'Back');
                }
            }
        },
        // Call this method when the language is selected/changed in the form
        updateFilteredVoices(form, side) {
            const selectedLanguage = form['selected' + side + 'Language'];
            form['filtered' + side + 'Voices'] = this.availableVoices
                .filter(voice => voice.LanguageName === selectedLanguage)
                .sort((a, b) => a.Name.localeCompare(b.Name));

            // If the currently selected voice ID is not in the filtered list, reset it
            if (!form['filtered' + side + 'Voices'].some(voice => voice.Id === form['selected' + side + 'VoiceId'])) {
                form['selected' + side + 'VoiceId'] = form['filtered' + side + 'Voices'].length > 0 ? form['filtered' + side + 'Voices'][0].Id : '';
            }
        },
        updateVoiceOptions(termForm, side) {
            const selectedLanguage = termForm['selected' + side + 'Language'];
            termForm['filtered' + side + 'Voices'] = this.availableVoices.filter(voice => voice.LanguageName === selectedLanguage);
            if (termForm['filtered' + side + 'Voices'].length > 0) {
                termForm['selected' + side + 'VoiceId'] = termForm['filtered' + side + 'Voices'][0].Id;
            }
        },


        // { TERM CREATION }

        // Toggles the form for creating a new term
        async toggleCreatingTerm() {
            // Ensure atomic running of method
            if (this.isTogglingCreateTerm) return;
            this.isTogglingCreateTerm = true;

            // Clear creating term errors
            this.createTermError = null;
            // If opening create term menu
            if (!this.isCreatingNewTerm) {
                // Load available voices if not already loaded
                if (!this.availableVoices) {
                    await this.fetchPollyVoices();
                }
                // Resets the form for creating a new term
                if (!this.isCreatingNewTerm) {
                    this.termCreateForm = {
                        front_text: '',
                        back_text: '',
                        front_image: null,
                        back_image: null,
                        study_set: this.setDetail.id
                    };
                }
                // Set inputs for lang/voice to match below default voices
                this.initializeVoiceSelections(this.termCreateForm, {
                    front_voice_id: 'Joanna',
                    back_voice_id: 'Takumi'
                })
                this.isCreatingNewTerm = true;
                // Re-render dom with next tick, then scroll to creating new term form
                this.$nextTick(() => {
                    const createTermElement = document.getElementById("create-term-form");
                    if (createTermElement) {
                        createTermElement.scrollIntoView({ behavior: "smooth" });
                    }
                });
            }
            // If closing menu...
            else {
                this.isCreatingNewTerm = false;
            }

            this.isTogglingCreateTerm = false;
        },
        // Creates a new term
        async createNewTerm() {
            // Create new term
            this.createTermError = null;
            try {
                const createTermResponse = await axiosAuthInstance.post('/study_sets/terms/', {
                    sort_order: this.studyTerms.length,
                    front_text: this.termCreateForm.front_text,
                    back_text: this.termCreateForm.back_text,
                    front_voice_id: this.termCreateForm.selectedFrontVoiceId,
                    back_voice_id: this.termCreateForm.selectedBackVoiceId,
                    study_set: this.setDetail.id,
                });

                const imgUploadError = await this.updateTermImages(createTermResponse.data.id, this.termCreateForm);

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

        // Update selected image files
        onUpdateFrontImageSelected(event) {
            this.termEditForm.front_image = event.target.files[0];
        },
        onUpdateBackImageSelected(event) {
            this.termEditForm.back_image = event.target.files[0];
        },
        onCreateFrontImageSelected(event) {
            this.termCreateForm.front_image = event.target.files[0];
        },
        onCreateBackImageSelected(event) {
            this.termCreateForm.back_image = event.target.files[0];
        },


        // { UPDATING TERMS }

        // Enters edit mode for a specific term (or exits if null provided as the term)
        async toggleEditingTerm(term) {
            // Load available voices if not already loaded
            if (!this.availableVoices) {
                await this.fetchPollyVoices();
            }
            // If a term is supplied, set fields
            if (term) {
                this.termEditForm = { ...term };
                this.termEditForm.front_image = null;
                this.termEditForm.back_image = null;
                this.initializeVoiceSelections(this.termEditForm, term);
            }
            // Otherwise, stop editing term
            else {
                this.termEditForm = null;
            }
            this.editTermError = null;
        },
        // Updates the term
        async updateTerm() {
            try {
                const termUpdateBody = {
                    front_text: this.termEditForm.front_text,
                    back_text: this.termEditForm.back_text,
                    front_voice_id: this.termEditForm.selectedFrontVoiceId,
                    back_voice_id: this.termEditForm.selectedBackVoiceId,
                }

                // Return early if image upload(s) fail
                const imgUploadError = await this.updateTermImages(this.termEditForm.id, this.termEditForm);
                if (imgUploadError) {
                    this.editTermError = imgUploadError;
                    return;
                }

                await axiosAuthInstance.patch(`/study_sets/terms/${this.termEditForm.id}/`, termUpdateBody);
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
                    formData.append('file', imageForm.front_image);

                    const uploadImgResponse = await axiosAuthInstance.post('/uploads/images/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    });
                    imageUploadForm.front_image_id = uploadImgResponse.data.id;
                }
                if (imageForm.back_image) {
                    const formData = new FormData();
                    formData.append('file', imageForm.back_image);

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
                await axiosAuthInstance.patch(`/study_sets/terms/${studyTermId}/`, imageUploadForm);
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

                    await axiosAuthInstance.patch(`/study_sets/terms/${this.termEditForm.id}/`, removeImageRequestBody);
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
                await axiosAuthInstance.delete(`study_sets/terms/${termId}/`);
                this.fetchSetTerms()
            } catch (error) {
                this.editTermError = extractFirstErrorMessage(error);
            }
        },


        // { PLAY TERM AUDIO }

        speak(side, term) {
            let audioPath = '';
            if (side === 'front' && term.front_tts_audio) {
                audioPath = term.front_tts_audio.file_path;
            } else if (side === 'back' && term.back_tts_audio) {
                audioPath = term.back_tts_audio.file_path;
            }

            if (audioPath) {
                const audio = new Audio(audioPath);
                audio.play().catch(e => console.error("Error playing audio:", e));
            } else {
                alert("No TTS audio available for this term.");
            }
        },


        // { REORDERING TERMS }

        // Toggle mode for editing order of study terms
        async toggleChangingOrder() {
            if (this.isTogglingChangeOrderMode) return;
            this.isTogglingChangeOrderMode = true;

            // If exiting changing mode, save changes
            if (this.isChangingOrder) {
                await this.updateSortOrder();
                this.studyTermOrders = null;
                this.isChangingOrder = false;
            }
            // If we're entering changing mode, cancel any term creation/editing
            else {
                this.toggleEditingTerm(null);
                if (this.isCreatingNewTerm) {
                    this.toggleCreatingTerm();
                }
                // Reset orders
                this.studyTermOrders = this.studyTerms.map(term => ({
                    id: term.id,
                }));
                this.isChangingOrder = true;
            }
            this.isTogglingChangeOrderMode = false;
        },
        // API call to update terms' orders
        async updateSortOrder() {
            // Get the container of the terms
            const termsList = document.querySelector('.terms-list');

            // Create an array from the children of the terms list and map to extract the id and sort order
            const sortOrderData = Array.from(termsList.children).map((termElement, index) => {
                // Extracting the numeric ID from the id attribute (e.g., "studyTermId=40" -> "40")
                const termId = termElement.id.match(/studyTermId=(\d+)/)[1];
                return {
                    id: termId,
                    sort_order: index
                };
            });

            // Send the updated sort order to the backend
            try {
                await axiosAuthInstance.post(`/study_sets/${this.setDetail.id}/update_term_order/`, {
                    term_order: sortOrderData
                });
                // Refetch the terms to ensure order consistency
                this.fetchSetTerms();
            } catch (error) {
                console.error("Error updating term order:", error);
            }
        },
    }
};
</script>


<style scoped>
/* Main div holding set information/edit sections */
.set-banner {
    position: relative;
}

/* Place Set-Edit button in top right of set banner */
.set-banner>button {
    position: absolute;
    top: var(--text-padding-400);
    right: var(--text-padding-400);
}

/* Targets favorite button in set-banner display, overrides rules above */
.set-banner .favorite-btn {
    left: var(--text-padding-400) !important;
    margin-right: var(--text-padding-400);
}

.set-banner .btn-stack {
    margin-left: var(--text-padding-400);
}

/* Set title */
.set-banner h1 {
    padding: var(--text-padding-400) var(--text-padding-1100) 0 var(--text-padding-1100);
}

/* Set description */
.set-banner p {
    padding: var(--text-padding-250) var(--text-padding-1000) var(--text-padding-400) var(--text-padding-1000);
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
    margin-bottom: var(--text-padding-300);
    padding: var(--text-padding-250) var(--text-padding-1100) var(--text-padding-250) var(--text-padding-250);
    height: var(--text-padding-1000);
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Set description input */
.set-banner textarea {
    margin-bottom: var(--text-padding-300);
    padding: var(--text-padding-250) var(--text-padding-1100) var(--text-padding-250) var(--text-padding-250);
    height: 6rem;
    width: 100%;
    resize: none;
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Set privacy input */
.set-banner select {
    padding-right: var(--text-padding-1100);
    width: 100%;
}


/* TERMS CSS OPTIONS */

/* Set background outside of terms list */
.terms-list {
    background-color: var(--clr-primary-250);
}

/* Terms buttons menu */
.term-btn-menu {
    position: sticky;
    top: var(--magnified-btn-size);
}

/* Level 1 term container, contains:
    - div/form : .term-display
    - div : .btn-stack
*/
.term-container {
    display: flex;
    gap: var(--text-padding-400);
    flex-direction: column;
    width: 100%;
    border: 1px solid #ddd;
    background-color: #f8f8f8;
}

/* Level 2 term container, sets basic padding and contains:
    - div/form : .term-info-display
    - div : .btn-stack
*/
.term-display {
    display: flex;
    gap: var(--text-padding-400);
    flex-direction: row;
    padding: var(--text-padding-400);
    width: 100%;
}

/* Level 3 term container, the non-btn-stack half with display/inputs.
    Contains:
        - span : .term-info-display span
            (display front card info)
        - span : .term-info-display span
            (display back card info)
*/
.term-info-display {
    flex: 1 1 auto;
    display: flex;
    flex-direction: row;
    /* Ensure maximum width stays below .btn-stack's position */
    max-width: calc(100% - var(--text-padding-1100));
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
.term-info-display span {
    display: flex;
    gap: var(--text-padding-250);
    justify-content: center;
    cursor: pointer;
}

/* Level 5 term container, ONLY in display format */
:not(form)>.term-info-display span {
    padding-top: var(--text-padding-400);
    padding-bottom: var(--text-padding-400);
}

/* Term image selectors */
.term-info-display>input,

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

/* Button to remove images */
.term-info-display picture button {
    position: absolute;
    left: var(--text-padding-250);
    top: var(--text-padding-250);
    border-radius: 12px !important;
    border: 2px solid white;
}

.term-info-display picture button:hover {
    opacity: 1 !important;
    background-color: rgb(248, 84, 84);
    border: 2px solid rgb(250, 100, 100);
}

/* Term front/back textarea input */
.term-info-display textarea {
    width: 100%;
    resize: vertical;
}

/* term-display class, but for changing sort_order view */
.term-display-reorder {
    align-items: center;
}

/* Symbol for reordering terms */
.reorder-symbol {
    color: black;
    width: var(--text-padding-1000);
    height:var(--text-padding-500);
    min-width: var(--text-padding-1000);
    min-height:var(--text-padding-500);
}

/* Make sure that the controls menu adjusts for the shorter top bar in desktop */
@media screen and (min-width: 768px) {
    .term-btn-menu {
        top: var(--default-btn-size);
    }
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