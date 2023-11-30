<template>
    <div class="set-container">
        <h1>My Study Sets</h1>
        <div v-if="error" class="error-message">{{ error }}</div>
        <button @click="toggleModal">Create New Set</button>
        <div class="sets-list" v-if="public_sets">
            <div class="set-item" v-for="set in public_sets" :key="set.id">
                <router-link class="info-panel" :to="`/my-study-set/${set.id}`">
                    <h3>{{ set.title }}</h3>
                    <p>{{ set.description || "No description provided." }}</p>
                </router-link>
                <button class="edit-button" @click="prepareEditSet(set)">Edit</button>
                <button class="delete-button" @click="confirmDelete(set.id)">Delete</button>
            </div>
        </div>
        <div class="pagination">
            <button @click="navigatePage('previous')" :disabled="!pagination_links.previous">Previous</button>
            <span>Page {{ current_page }} of {{ total_pages }}</span>
            <button @click="navigatePage('next')" :disabled="!pagination_links.next">Next</button>
        </div>
        <ModalComponent :showModal="showModal" @update:showModal="showModal = $event">
            <form @submit.prevent="submitForm">
                <div v-if="modal_error" class="error-message">{{ modal_error }}</div>
                <label for="title">Title:</label>
                <input type="text" id="title" v-model="study_set_form.title" required>
                <label for="description">Description:</label>
                <textarea id="description" v-model="study_set_form.description"></textarea>
                <label for="private">Private:</label>
                <input type="checkbox" id="private" v-model="study_set_form.private">
                <div class="modal-footer">
                    <button type="button" @click="toggleModal">Cancel</button>
                    <button type="submit">{{ isEditMode ? 'Update Set' : 'Create Set' }}</button>
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
            error: null,
            public_sets: null,
            pagination_links: {},
            current_page: 1,
            total_pages: 1,
            showModal: false,
            isEditMode: false,
            editingSetId: null,
            modal_error: null,
            study_set_form: {
                title: '',
                description: '',
                private: false,
            }
        };
    },
    methods: {
        toggleModal() {
            this.showModal = !this.showModal;
            if (!this.showModal) {
                this.resetForm();
            }
        },
        resetForm() {
            this.isEditMode = false;
            this.editingSetId = null;
            this.study_set_form = { title: '', description: '', private: false };
        },
        prepareEditSet(set) {
            this.isEditMode = true;
            this.editingSetId = set.id;
            this.study_set_form = { ...set };
            this.showModal = true;
        },
        async submitForm() {
            this.modal_error = null;
            if (this.study_set_form.title == '') {
                this.modal_error = "Please enter a title for your Study Set!";
                return;
            }
            try {
                if (this.isEditMode) {
                    await axiosAuthInstance.put(`study_sets/study_sets/${this.editingSetId}/`, this.study_set_form);
                } else {
                    await axiosAuthInstance.post('study_sets/study_sets/', this.study_set_form);
                }
                this.toggleModal();
                this.getMyStudySets(this.current_page);
            } catch (error) {
                this.modal_error = error.response ? error.response.data.detail : "An error occurred while processing the set.";
            }
        },
        confirmDelete(setId) {
            if (confirm("Are you sure you want to delete this set?")) {
                this.deleteStudySet(setId);
            }
        },
        async deleteStudySet(setId) {
            try {
                await axiosAuthInstance.delete(`study_sets/study_sets/${setId}/`);
                this.getMyStudySets(this.current_page); // Refresh the list after deletion
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred while deleting the set';
            }
        },
        async getMyStudySets(page) {
            this.error = null;
            try {
                const response = await axiosAuthInstance.get(`study_sets/my_sets/?page=${page}`);
                this.public_sets = response.data.results;
                this.pagination_links = response.data.links;
                this.current_page = response.data.current_page;
                this.total_pages = response.data.total_pages;
            } catch (error) {
                this.error = error.response ? error.response.data.detail : 'An error occurred';
            }
        },
        navigatePage(direction) {
            const nextPage = direction === 'next' ? this.current_page + 1 : this.current_page - 1;
            this.$router.push({ path: '/my-study-sets/' + nextPage.toString() });
        }
    },
    watch: {
        '$route.params.page': {
            immediate: true,
            handler(newPage) {
                this.getMyStudySets(newPage || 1);
            }
        }
    },
    mounted() {
        const initialPage = this.$route.params.page || 1;
        this.getMyStudySets(initialPage);
    }
}
</script>

<!-- <style scoped>
/* @import "@/assets/container-list-style.css"; */
</style> -->

<style scoped>
.set-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

.sets-list {
    margin-top: 20px;
}

.set-item {
    display: flex;
    align-items: center;
    justify-content: right;
    background-color: #f8f8f8;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
}

.set-item a {
    display: inline-block;
    flex-grow: 1;
    margin-left: 1rem;
    text-align: left;
}

.set-item h3 {
    display: inline-block;
    width: 50%;
    font-size: 1.2em;
}

.set-item p {
    display: inline-block;
    width: 50%;
    color: #666;
    font-size: 0.9em;
}

.set-item button {
    margin-left: 10px;
    padding: 5px 10px;
    font-size: 0.9em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.set-item button:hover {
    opacity: 0.9;
}

.set-item .edit-button {
    display: inline-block;
    width: 8rem;
    max-width: 8rem;
    height: 3rem;
    background-color: #4CAF50;
    color: white;
}

.set-item .delete-button {
    width: 5rem;
    max-width: 5rem;
    height: 3rem;
    background-color: #f44336;
    color: white;
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

.error-message {
    color: #f44336;
    text-align: center;
    margin-top: 10px;
}
</style>
