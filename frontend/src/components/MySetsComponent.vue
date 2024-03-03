<template>
    <main>
        <section id="page-topper"><span>My Sets</span></section>
        <h1 class="main-header">My Study Sets</h1>
        <!-- Inline Form for Creating a New Study Set -->
        <div class="set-container set-edit set-creator" v-if="creatingNewSet">
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
                <button @click="createSet" class="square-btn green-btn"><font-awesome-icon class="fa-icon"
                        :icon="['fas', 'plus']" /></button>
                <button @click="toggleCreateNewSet" class="square-btn yellow-btn"><font-awesome-icon class="fa-icon"
                        :icon="['fas', 'ban']" /></button>
            </div>
        </div>

        <div class="control-bar">
            <button @click="toggleCreateNewSet" :disabled="creatingNewSet">Create New Set</button>
        </div>

        <!-- List of Study Sets -->
        <section v-for="set in public_sets" :key="set.id" class="set-list">
            <div v-if="editingSetId === set.id" class="set-container set-edit">
                <!-- Editable Fields for a Study Set -->
                <button @click.prevent="toggleFavorite(set)" class="square-btn transparent-btn favorite-btn"><font-awesome-icon class="fa-icon"
                        :icon="[set.favorited ? 'fas' : 'far', 'star']" /></button>
                <div>
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
                    <button @click="editSet(null)" class="square-btn yellow-btn"><font-awesome-icon class="fa-icon"
                            :icon="['fas', 'ban']" /></button>
                    <button @click="confirmDeleteSet(set.id)" class="square-btn red-btn"><font-awesome-icon class="fa-icon"
                            :icon="['fas', 'trash-alt']" /></button>
                </div>
            </div>
            <router-link v-else :to="`/my-study-set/${set.id}`" class="set-container set-display">
                <!-- Displaying Study Set Details -->
                <button @click.prevent="toggleFavorite(set)" class="square-btn transparent-btn favorite-btn"><font-awesome-icon class="fa-icon"
                        :icon="[set.favorited ? 'fas' : 'far', 'star']" /></button>
                <div>
                    <h2>{{ set.title }}</h2>
                    <p>{{ set.description }}</p>
                </div>
                <button @click.prevent="editSet(set)" class="square-btn transparent-btn"><font-awesome-icon class="fa-icon"
                        :icon="['fas', 'edit']" /></button>
            </router-link>
        </section>

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
/* List container for sets */

.set-list {
    background-color: var(--clr-primary-50);
}

/* Level 1 container of set information */
/* SET VIEW (a block) */

.set-container {
    display: flex;
    gap: var(--text-padding-400);
    width: 100%;
    padding: var(--text-padding-400);
    border: 1px solid var(--clr-neutral-300);
    background-color: var(--clr-neutral-250);
    align-items: center;
    text-align: left;
}

/* Level 2 container of set information, holds display information
    - Set display should grow to cover empty space between buttons */

.set-container div {
    flex-grow: 1;
}

/* Make sure display doesn't push list item off of screen,
    - But ensure it doesn't limit the size allowed in set creator */

.set-container:not(.set-creator) div {
    max-width: calc(100% - (2 * var(--text-padding-400)) - (2 * var(--default-btn-size)));
}

/* Color in the favorite button */

.favorite-btn {
    color: var(--clr-util-warning);
}

/* Make sure set title doesn't wrap, style... */

.set-display h2 {
    overflow: hidden;
    white-space: nowrap;
    color: var(--clr-neutral-1000);
    font-size: var(--fs-500);
    font-weight: var(--fw-semi-bold);
}

/* Keep description within specific height bounds, style... */

.set-display p {
    overflow: hidden;
    line-height: 1.6rem;
    max-height: 3.2rem;
    padding-left: 0.25rem;
    color: var(--clr-primary-900);
    font-size: var(--fs-300);
}

/* SET EDIT */

/* Set title input editor */

.set-edit input {
    width: 100%;
    height: 2rem;
    font-size: var(--fs-500);
    font-weight: var(--fw-semi-bold);
}

/* Set description textarea editor */

.set-edit textarea {
    padding: 0.05rem;
    width: 100%;
    height: 5.6rem;
    font-size: var(--fs-300);
}

/* Set visibility select label editor */

.set-edit span {
    display: block;
    padding: var(--text-padding-250);
    width: 100%;
    font-weight: var(--fw-bold);
}

/* When <main> is at least: DESKTOP MEDIA QUERY */
@container (min-width: 1000px) {
    /* List container for sets */

    .set-list {
        padding-left: 13%;
        padding-right: 13%;
    }
}
</style>