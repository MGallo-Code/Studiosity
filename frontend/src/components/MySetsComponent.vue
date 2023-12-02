<template>
    <div class="set-container">
        <h1>My Study Sets</h1>
        <div v-if="error" class="error-message">{{ error }}</div>

        <!-- Create New Set - Inline Form -->
        <div class="set-item new-set-form" v-if="creatingNewSet">
            <input type="text" placeholder="Set Title" v-model="newSet.title" />
            <textarea placeholder="Set Description" v-model="newSet.description"></textarea>
            <button @click="createSet">Create</button>
        </div>

        <button @click="toggleCreateNewSet">Create New Set</button>

        <!-- Study Sets List -->
        <div class="sets-list">
            <div class="set-item" v-for="set in public_sets" :key="set.id">
                <div v-if="editingSetId === set.id">
                    <input type="text" v-model="set.title" />
                    <textarea v-model="set.description"></textarea>
                    <select v-model="set.private">
                        <option value="false">Public</option>
                        <option value="true">Private</option>
                    </select>
                    <button @click="updateSet(set)">✔</button>
                    <button @click="deleteSet(set.id)">Delete</button>
                </div>
                <div v-else>
                    <router-link :to="`/my-study-set/${set.id}`">{{ set.title }}</router-link>
                    <p>{{ set.description }}</p>
                    <button @click="editSet(set)">✏️</button>
                </div>
            </div>
        </div>

        <!-- Pagination -->
        <div class="pagination">
            <button @click="navigatePage('previous')" :disabled="!pagination_links.previous">Previous</button>
            <span>Page {{ current_page }} of {{ total_pages }}</span>
            <button @click="navigatePage('next')" :disabled="!pagination_links.next">Next</button>
        </div>
    </div>
</template>

<script>
import { axiosAuthInstance } from '../utils/axios-config';

export default {
    data() {
        return {
            error: null,
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
        toggleCreateNewSet() {
            this.creatingNewSet = !this.creatingNewSet;
            if (!this.creatingNewSet) {
                this.resetNewSetForm();
            }
        },
        resetNewSetForm() {
            this.newSet = { title: '', description: '', private: false };
        },
        createSet() {
            // API call to create a new set
            axiosAuthInstance.post('/study_sets/study_sets/', this.newSet)
                .then(response => {
                    this.public_sets.push(response.data);
                    this.toggleCreateNewSet();
                })
                .catch(error => {
                    this.error = error.response ? error.response.data.message : 'Error creating set';
                });
        },
        editSet(set) {
            this.editingSetId = set.id;
        },
        updateSet(set) {
            // API call to update the set
            axiosAuthInstance.put(`/study_sets/study_sets/${set.id}/`, set)
                .then(() => {
                    this.editingSetId = null;
                    // Optionally refresh the list of sets
                })
                .catch(error => {
                    this.error = error.response ? error.response.data.message : 'Error updating set';
                });
        },
        deleteSet(setId) {
            // API call to delete the set
            axiosAuthInstance.delete(`/study_sets/study_sets/${setId}/`)
                .then(() => {
                    this.public_sets = this.public_sets.filter(set => set.id !== setId);
                })
                .catch(error => {
                    this.error = error.response ? error.response.data.message : 'Error deleting set';
                });
        },
            navigatePage(direction) {
            const nextPage = direction === 'next' ? this.current_page + 1 : this.current_page - 1;
            this.getMyStudySets(nextPage);
        },
        getMyStudySets(page) {
            axiosAuthInstance.get(`/study_sets/my_sets/?page=${page}`)
                .then(response => {
                    this.public_sets = response.data.results;
                    this.pagination_links = response.data.links;
                    this.current_page = response.data.current_page;
                    this.total_pages = response.data.total_pages;
                })
                .catch(error => {
                    this.error = error.response ? error.response.data.message : 'Error fetching sets';
                });
        },
    },
    mounted() {
        // Fetch initial data
        this.getMyStudySets(1);
    }
};
</script>

<style scoped>
.set-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

.sets-list, .new-set-form {
    margin-top: 20px;
}

.set-item {
    background-color: #f8f8f8;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
}

.set-item input, .set-item textarea {
    width: 100%;
    margin-bottom: 10px;
}

.set-item select {
    margin-bottom: 10px;
}

.set-item button {
    padding: 5px 10px;
    margin-right: 5px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.error-message {
    color: #f44336;
    text-align: center;
    margin-top: 10px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.pagination button {
    margin: 0 5px;
    padding: 5px 10px;
    font-size: 1em;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}

.pagination button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>
