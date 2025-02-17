<template>
    <main>
        <section id="page-topper"><span>My Profile</span></section>
        <h1 class="main-header">Edit My Profile</h1>

        <!-- User Profile Display -->
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
    </main>
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
                        this.profileImage = response.data.profile_image.file_path;
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
                    formData.append('file', this.editableProfile.file);

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
                if (error.response?.data?.username
                    && error.response?.data?.username[0] == "user model with this username already exists.") {
                    this.error = "This username is taken. Please choose another name."
                } else {
                    this.error = extractFirstErrorMessage(error);
                }
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

<style scoped>
/* --- MY PROFILE DISPLAY --- */
.my-profile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Optional spacing & max width */
    margin: var(--text-padding-700) auto;
    max-width: 600px;
    gap: var(--text-padding-300);
}

/* Keep or adjust image style as desired */
.my-profile-container img {
    object-fit: cover;
    width: 20rem;
    height: 20rem;
    border-radius: 100%;
    border: 2px solid var(--clr-primary-600); /* Example token usage */
}

.my-profile-container h1 {
    margin: 0;
    font-size: var(--fs-600);
    font-weight: var(--fw-bold);
}

.my-profile-container p {
    font-size: var(--fs-400);
    text-align: center;
    margin: 0;
}

/* --- PROFILE EDIT FORM --- */
.profile-edit-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Spacing & sizing */
    gap: var(--text-padding-300);
    max-width: 600px;
    margin: var(--text-padding-400) auto;
}

.profile-edit-form .error-message {
    color: var(--clr-util-error);
    text-align: center;
    padding: var(--text-padding-300);
    margin: 0; /* Remove default paragraph spacing */
}

.profile-edit-form input[type="file"],
.profile-edit-form input[type="text"],
.profile-edit-form textarea {
    width: 80%;
    max-width: 500px;
    padding: var(--text-padding-250);
    border: 1px solid var(--clr-neutral-300);
    border-radius: var(--default-border-radius);
    font-size: var(--fs-400);
    font-family: var(--ff-body);
}

.profile-edit-form textarea {
    min-height: 6rem; /* Provide a bit more vertical space for user bio */
    resize: vertical; /* Let user expand the textarea if needed */
}

.profile-edit-form button {
    background-color: var(--clr-primary-600);
    color: var(--clr-neutral-0);
    font-size: var(--fs-button);
    font-weight: var(--fw-bold);
    border-radius: var(--default-border-radius);
    border: none;
    cursor: pointer;
    height: var(--default-btn-size);

    /* Sizing & alignment */
    width: 50%;
    max-width: 15rem;
    margin-top: var(--text-padding-300);
}
</style>