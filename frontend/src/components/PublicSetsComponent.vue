<template>
    <div class="public-sets-container">
        <h1>My Study Sets</h1>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="public_sets">
            <div v-for="set in public_sets" :key="set.id">
                <h3>{{ set.title }}</h3>
            </div>
        </div>
    </div>
</template>

<script>
import axiosInstance from '../utils/axios-config';

export default {
  data() {
    return {
      error: null,
      public_sets: null,
    };
  },
  methods: {
    async getPublicStudySets() {
      // Reset error on new submission
      this.error = null;

      try {
        let response = await axiosInstance.get('study_sets/public_sets/');
        this.public_sets = response.data.results;
      } catch (error) {
        this.error = error.response.data.detail;
      }
    }
  },
  mounted() {
    this.getPublicStudySets()
  }
}
</script>

<!-- Add styles as needed -->
<style>
/* Your CSS here */
</style>