<template>
    <main>
        <section id="main-header"><span>My Sets</span></section>
        <h1>My Study Sets</h1>
        <!-- Inline Form for Creating a New Study Set -->
        <div class="set-container set-edit" v-if="creatingNewSet">
            <div class="edit-inputs">
                <p v-if="createSetError" class="error-message">{{ createSetError }}</p>
                <input type="text" placeholder="Set Title" v-model="newSet.title" />
                <textarea placeholder="Set Description" v-model="newSet.description"></textarea>
                <span>
                    Visibility:
                    <select v-model="newSet.private">
                        <option value="false">Public</option>
                        <option value="true">Private</option>
                    </select>
                </span>
            </div>
            <div class="btn-stack">
                <button @click="createSet" class="square-btn green-btn"><font-awesome-icon
                        :icon="['fas', 'plus']" /></button>
                <button @click="toggleCreateNewSet" class="square-btn yellow-btn"><font-awesome-icon
                        :icon="['fas', 'ban']" /></button>
            </div>
        </div>

        <button @click="toggleCreateNewSet" :disabled="creatingNewSet">Create New Set</button>

        <!-- List of Study Sets -->
        <div v-for="set in public_sets" :key="set.id">
            <div v-if="editingSetId === set.id" class="set-container set-edit">
                <!-- Editable Fields for a Study Set -->
                <button @click.prevent="toggleFavorite(set)" class="favorite-btn square-btn"><font-awesome-icon
                        :icon="[set.favorited ? 'fas' : 'far', 'star']" /></button>
                <div class="edit-inputs">
                    <p v-if="editSetError" class="error-message">{{ editSetError }}</p>
                    <input type="text" v-model="set.title" />
                    <textarea v-model="set.description"></textarea>
                    <span>
                        Visibility:
                        <select v-model="set.private">
                            <option value="false">Public</option>
                            <option value="true">Private</option>
                        </select>
                    </span>
                </div>
                <div class="btn-stack">
                    <button @click="updateSet(set)" class="square-btn green-btn">✔</button>
                    <button @click="editSet(null)" class="square-btn yellow-btn"><font-awesome-icon
                            :icon="['fas', 'ban']" /></button>
                    <button @click="confirmDeleteSet(set.id)" class="square-btn red-btn"><font-awesome-icon
                            :icon="['fas', 'trash-alt']" /></button>
                </div>
            </div>
            <router-link v-else :to="`/my-study-set/${set.id}`" class="set-container set-display">
                <!-- Displaying Study Set Details -->
                <button @click.prevent="toggleFavorite(set)" class="favorite-btn square-btn"><font-awesome-icon
                        :icon="[set.favorited ? 'fas' : 'far', 'star']" /></button>
                <div>
                    <h2>{{ set.title }}</h2>
                    <p>{{ set.description }}</p>
                </div>
                <button @click.prevent="editSet(set)" class="square-btn blue-btn"><font-awesome-icon
                        :icon="['fas', 'edit']" /></button>
            </router-link>
        </div>

        <!-- Pagination Controls -->
        <div class="pagination">
            <button @click="navigatePage('previous')" :disabled="!pagination_links.previous">Previous</button>
            <span>Page {{ current_page }} of {{ total_pages }}</span>
            <button @click="navigatePage('next')" :disabled="!pagination_links.next">Next</button>
        </div>
    </main>
</template>
  
<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        return {
            // Initialize component state
            createSetError: null,
            editSetError: null,
            public_sets: [],
            pagination_links: {},
            current_page: 1,
            total_pages: 1,
            creatingNewSet: false,
            editingSetId: null,
            newSet: { title: '', description: '', private: false },
        };
    },
    methods: {
        // Toggle visibility of inline form for creating new sets
        toggleCreateNewSet() {
            this.creatingNewSet = !this.creatingNewSet;
            if (!this.creatingNewSet) {
                this.resetNewSetForm();
                this.createSetError = null;
            }
        },
        // Reset form fields for new set creation
        resetNewSetForm() {
            this.newSet = { title: '', description: '', private: false };
        },
        // API call to create a new study set
        createSet() {
            axiosAuthInstance.post('/study_sets/', this.newSet)
                .then(response => {
                    this.public_sets.push(response.data);
                    this.toggleCreateNewSet();
                    this.createSetError = null;
                })
                .catch(error => {
                    this.createSetError = extractFirstErrorMessage(error);
                });
        },
        // Set the current set to be edited
        editSet(set) {
            this.editingSetId = set ? set.id : null;
            this.editSetError = null;
        },
        // API call to update the study set
        updateSet(set) {
            axiosAuthInstance.put(`/study_sets/${set.id}/`, set)
                .then(() => {
                    this.editingSetId = null;
                    this.editSetError = null;
                })
                .catch(error => {
                    this.editSetError = extractFirstErrorMessage(error);
                });
        },
        // Confirms and deletes a set
        async confirmDeleteSet(termId) {
            if (confirm("Are you sure you want to delete this set?")) {
                await this.deleteSet(termId);
            }
        },
        // API call to delete the study set
        deleteSet(setId) {
            axiosAuthInstance.delete(`/study_sets/${setId}/`)
                .then(() => {
                    this.public_sets = this.public_sets.filter(set => set.id !== setId);
                })
                .catch(error => {
                    this.editSetError = extractFirstErrorMessage(error);
                });
        },
        // Navigate through paginated study sets
        navigatePage(direction) {
            const nextPage = direction === 'next' ? this.current_page + 1 : this.current_page - 1;
            this.getMyStudySets(nextPage);
        },
        // Fetch study sets for the current page
        getMyStudySets(page) {
            axiosAuthInstance.get(`/study_sets/my_sets/?page=${page}`)
                .then(response => {
                    this.public_sets = response.data.results;
                    this.pagination_links = response.data.links;
                    this.current_page = response.data.current_page;
                    this.total_pages = response.data.total_pages;
                })
                .catch(error => {
                    console.log(error.response ? error.response.data.message : 'Error fetching sets');
                });
        },
        // Toggle favorite/unfavorite for a study set
        toggleFavorite(set) {
            axiosAuthInstance.post(`/study_sets/${set.id}/favorite/`)
                .then(response => {
                    set.favorited = response.data.status === 'favorited';
                })
                .catch(error => {
                    console.error("Error toggling favorite status:", error.response ? error.response.data : error);
                });
        },
    },
    mounted() {
        // Initial data fetch when the component is mounted
        this.getMyStudySets(1);
    }
};
</script>

<style scoped>
.set-container {
    width: calc(100% - 2rem);
    height: calc(100% - 2rem);
    margin: 0 1rem 0.8rem 1rem;
    padding: 0;
    border-radius: 0.35rem;
    border: 1px solid #ddd;
    background-color: #f0f0f0;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.set-container:hover {
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}

/* SET VIEW (a block) */

.favorite-btn {
    margin-right: 1rem;
    font-size: 1.2rem;
    color: var(--clr-btn-yellow) !important;
    background-color: inherit !important;
}

.favorite-btn:hover {
    background-color: #e0e0e0 !important;
}

.set-display {
    display: flex;
    align-items: center;
    padding: 1rem;
}

.set-display div {
    flex-grow: 1;
    text-align: left;
    padding-right: 1rem;
}

.set-display h2 {
    color: var(--clr-base-primary);
}

.set-display p {
    overflow: hidden;
    max-height: 3rem;
    padding-left: 0.2rem;
    color: black;
}

/* SET EDIT */

.set-edit {
    display: flex;
    padding: 1rem;
}

/* div with set edit inputs */

.edit-inputs {
    flex-grow: 1;
}

.set-edit input {
    width: 100%;
    height: 2rem;
    font-size: 1.4rem;
}

.set-edit textarea {
    padding: 0.05rem;
    width: 100%;
    height: 5.6rem;
    font-size: 1rem;
}

.set-edit span {
    display: block;
    padding: 0.4rem;
    width: 100%;
    text-align: left;
    font-weight: 800;
}
</style>
