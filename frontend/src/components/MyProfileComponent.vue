<template>
    <div v-if="profile" class="my-profile-container">
        <img :src="profileImage" alt="Profile Picture" />
        <h1>{{ profile.username }}</h1>
        <p>{{ profile.bio || 'No user bio provided.' }}</p>
    </div>

    <!-- Editing Form -->
    <div class="profile-edit-form">
        <p class="error-message">{{ error }}</p>
        <input type="file" @change="onFileSelected" />
        <input type="text" v-model="editableProfile.username" placeholder="Username" />
        <textarea v-model="editableProfile.bio" placeholder="Bio"></textarea>
        <button @click="submitProfileUpdate">Submit Changes</button>
    </div>
</template>

<script>
import { axiosAuthInstance } from '../utils/axiosConfig';
import { mapState } from 'vuex';
import DefaultProfile from '@/assets/default-profile-picture.png';
import { extractFirstErrorMessage } from '@/utils/errorHandler';

export default {
    data() {
        return {
            profile: null,
            editableProfile: {
                username: '',
                bio: '',
                profileImage: '',
            },
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
        onFileSelected(event) {
            this.editableProfile.file = event.target.files[0];
        },
        async submitProfileUpdate() {
            this.error = null;
            try {
                const profileUpdateBody = {
                    username: this.editableProfile.username,
                    bio: this.editableProfile.bio,
                }

                // If a new file was selected, upload it first
                if (this.editableProfile.file) {
                    const formData = new FormData();
                    formData.append('file_path', this.editableProfile.file);

                    const uploadImgResponse = await axiosAuthInstance.post('/uploads/images/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    });

                    // Only add profile_image to the update body if a new file was uploaded
                    profileUpdateBody.profile_image = uploadImgResponse.data.id;
                }

                // Update user profile
                await axiosAuthInstance.patch(`/users/update/${this.profile.id}/`, profileUpdateBody);

                this.getUserProfile(); // Refresh the profile
            } catch (error) {
                this.error = extractFirstErrorMessage(error);
            }
        },
    },
    watch: {
        profile: {
            handler(newProfile) {
                if (newProfile) {
                    this.editableProfile.username = newProfile.username;
                    this.editableProfile.bio = newProfile.bio;
                    this.editableProfile.profileImage = newProfile.profile_image || DefaultProfile;
                }
            },
            deep: true,
        },
    },
};
</script>

<style>
.my-profile-container img {
    object-fit: cover;
    width: 20rem;
    height: 20rem;
    border-radius: 100%;
    border: 2px solid var(--clr-base-primary);
}
</style>
