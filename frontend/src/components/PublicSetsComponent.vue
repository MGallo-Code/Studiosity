<template>
  <div class="set-container">
      <h1>Public Study Sets</h1>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div class="sets-list" v-if="public_sets">
        <router-link 
          v-for="set in public_sets" 
          :key="set.id" 
          :to="`/study-set/${set.id}`" 
        >
            <div class="set-item">
              <h3>{{ set.title }}</h3>
              <p>{{ set.description || "No description provided." }}</p>
            </div>
        </router-link>
      </div>
      <div class="pagination">
          <button @click="navigatePage('previous')" :disabled="!pagination_links.previous">Previous</button>
          <span>Page {{ current_page }} of {{ total_pages }}</span>
          <button @click="navigatePage('next')" :disabled="!pagination_links.next">Next</button>
      </div>
  </div>
</template>

<script>
import { axiosDefaultInstance } from '../utils/axios-config';

export default {
  data() {
    return {
      error: null,
      public_sets: null,
      pagination_links: {},
      current_page: 1,
      total_pages: 1,
    };
  },
  methods: {
    async getPublicStudySets(page) {
      this.error = null;

      try {
        const response = await axiosDefaultInstance.get(`study_sets/study_sets/?page=${page}`);
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
      this.$router.push({ path: '/public-study-sets/' + nextPage.toString() });
    }
  },
  watch: {
    '$route.params.page': {
      immediate: true,
      handler(newPage) {
        this.getPublicStudySets(newPage || 1);
      }
    }
  },
  mounted() {
    const initialPage = this.$route.params.page || 1;
    this.getPublicStudySets(initialPage);
  }
}
</script>