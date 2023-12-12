<template>
    <!-- Set Container for My Study Sets Page -->
    <div class="set-container">
        <h1>My Study Sets</h1>
        <div v-if="error" class="error-message">{{ error }}</div>
    
        <!-- Inline Form for Creating a New Study Set -->
        <div class="set-item new-set-form" v-if="creatingNewSet">
            <input type="text" placeholder="Set Title" v-model="newSet.title" />
            <textarea placeholder="Set Description" v-model="newSet.description"></textarea>
            <select v-model="newSet.private">
                <option value="false">Public</option>
                <option value="true">Private</option>
            </select>
            <button @click="createSet">Create</button>
            <button @click="toggleCreateNewSet">Cancel</button> <!-- Cancel Button -->
        </div>
    
        <button @click="toggleCreateNewSet">Create New Set</button>
    
        <!-- List of Study Sets -->
        <div class="sets-list">
            <div class="set-item" v-for="set in public_sets" :key="set.id">
            <div v-if="editingSetId === set.id">
                <!-- Editable Fields for a Study Set -->
                <input type="text" v-model="set.title" />
                <textarea v-model="set.description"></textarea>
                <select v-model="set.private">
                <option value="false">Public</option>
                <option value="true">Private</option>
                </select>
                <button @click="updateSet(set)">✔</button>
                <button @click="deleteSet(set.id)"><font-awesome-icon icon="trash-alt" /></button>
            </div>
            <div v-else>
                <!-- Displaying Study Set Details -->
                <router-link :to="`/my-study-set/${set.id}`">{{ set.title }}</router-link>
                <p>{{ set.description }}</p>
                <button @click="editSet(set)"><font-awesome-icon icon="edit" /></button>
            </div>
            </div>
        </div>
    
        <!-- Pagination Controls -->
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
            // Initialize component state
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
        // Toggle visibility of inline form for creating new sets
        toggleCreateNewSet() {
            this.creatingNewSet = !this.creatingNewSet;
            if (!this.creatingNewSet) {
                this.resetNewSetForm();
            }
        },
        // Reset form fields for new set creation
        resetNewSetForm() {
            this.newSet = { title: '', description: '', private: false };
        },
        // API call to create a new study set
        createSet() {
            axiosAuthInstance.post('/study_sets/study_sets/', this.newSet)
            .then(response => {
                this.public_sets.push(response.data);
                this.toggleCreateNewSet();
            })
            .catch(error => {
                this.error = error.response ? error.response.data.message : 'Error creating set';
            });
        },
        // Set the current set to be edited
        editSet(set) {
            this.editingSetId = set.id;
        },
        // API call to update the study set
        updateSet(set) {
            axiosAuthInstance.put(`/study_sets/study_sets/${set.id}/`, set)
            .then(() => {
                this.editingSetId = null;
            })
            .catch(error => {
                this.error = error.response ? error.response.data.message : 'Error updating set';
            });
        },
        // API call to delete the study set
        deleteSet(setId) {
            axiosAuthInstance.delete(`/study_sets/study_sets/${setId}/`)
            .then(() => {
                this.public_sets = this.public_sets.filter(set => set.id !== setId);
            })
            .catch(error => {
                this.error = error.response ? error.response.data.message : 'Error deleting set';
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
                this.error = error.response ? error.response.data.message : 'Error fetching sets';
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
    max-width: 800px;
    margin: auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.sets-list, .new-set-form {
    margin-top: 20px;
}

.set-item {
    background-color: #f8f8f8;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.set-item input, .set-item textarea {
    width: 70%;
    margin-right: 10px;
}

.set-item select {
    margin-right: 10px;
}

.set-item button {
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: #4CAF50;
    color: white;
    margin-right: 5px;
}

.set-item button:hover {
    opacity: 0.9;
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

.font-awesome-icon {
    font-size: 1.2em;
}

.new-set-form {
    display: flex;
    flex-direction: column;
}

.new-set-form input, .new-set-form textarea {
    margin-bottom: 10px;
}

.new-set-form button {
    align-self: flex-start;
}
</style>
