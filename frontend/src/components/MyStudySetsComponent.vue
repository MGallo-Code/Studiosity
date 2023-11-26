<template>
    <div class="my-study-sets-container">
        <h1>My Study Sets</h1>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="my_sets">
            <div v-for="set in my_sets" :key="set.id">
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
      my_sets: null,
    };
  },
  methods: {
    async getMyStudySets() {
      // Reset error on new submission
      this.error = null;

      try {
        let response = await axiosInstance.get('study_sets/my_sets/');
        this.my_sets = response.data.results;
      } catch (error) {
        this.error = error.response.data.detail;
      }
    }
  },
  mounted() {
    this.getMyStudySets()
  }
}
</script>

<!-- Add styles as needed -->
<style>
/* Your CSS here */
</style>