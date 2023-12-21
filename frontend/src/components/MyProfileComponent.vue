<template>
    <p v-if="!this.profile" class="error-message"></p>
    <div v-else class="my-profile-container">
        <img class="profile-picture" :src="profileImage" alt="Profile Picture" />
        <h1>{{ this.profile.username }}</h1>


        <!-- <p>{{ profile.bio || 'No description provided.' }}</p> -->
    </div>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { mapState } from 'vuex';
import DefaultProfile from '@/assets/default-profile-picture.png';

export default {
    data() {
        return {
            profile: null,
            profileImage: DefaultProfile,
            error: null,
        };
    },
    computed: {
        ...mapState(['isAuthenticated'])
    },
    created() {
        this.getUserProfile();
    },
    methods: {
        async getUserProfile() {
            if (this.$store.state.isAuthenticated) {
                try {
                    const response = await axiosAuthInstance.get('/users/profile/');
                    if (response.data.profile_image) {
                        this.profileImage = response.data.profile_image;
                    }
                    this.profile = response.data;
                } catch (error) {
                    this.error = extractFirstErrorMessage(error);
                }
            }
        },
    },
};
</script>

<style>
.my-profile-container .profile-picture {
    max-width: 20%;
    border-radius: 0.6rem;
    border: 2px solid var(--clr-base-primary);
}
</style>
