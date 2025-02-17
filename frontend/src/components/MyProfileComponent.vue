<template>
    <main>
        <!-- Existing page topper / header remain untouched -->
        <section id="page-topper"><span>My Profile</span></section>
        <h1 class="main-header">Edit My Profile</h1>

        <!-- VIEW MODE (Read-only) -->
        <div
            v-if="profile && !editMode"
            class="my-profile-container"
        >
            <img :src="profileImage" alt="Profile Picture" />
            <h1>{{ profile.username }}</h1>
            <p>{{ profile.bio || 'No user bio provided.' }}</p>

            <!-- Toggle to Edit Mode -->
            <button @click="toggleEditMode">
                Edit Profile
            </button>
        </div>

        <!-- EDIT MODE (Show form) -->
        <div
            v-else-if="profile && editMode"
            class="profile-edit-form"
        >
            <p class="error-message" v-if="error">{{ error }}</p>

            <input
                type="file"
                @change="onFileSelected"
            />

            <input
                type="text"
                v-model="editableProfile.username"
                placeholder="Username"
            />

            <textarea
                v-model="editableProfile.bio"
                placeholder="Bio"
            ></textarea>

            <!-- Submit updates -->
            <button @click="submitProfileUpdate">
                Save Changes
            </button>
            <!-- Cancel editing (revert edits, hide form) -->
            <button class="cancel-btn" @click="cancelEdit">
                Cancel
            </button>
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
            editMode: false,
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

                // Refresh profile, then exit edit mode
                this.getUserProfile();
                this.editMode = false;
                
            } catch (error) {
                if (error.response?.data?.username
                    && error.response?.data?.username[0] == "user model with this username already exists.") {
                    this.error = "This username is taken. Please choose another name."
                } else {
                    this.error = extractFirstErrorMessage(error);
                }
            }
        },

        // Toggles whether or not the form is shown
        toggleEditMode() {
            // Copy the current read-only profile into editable fields
            this.editableProfile.username = this.profile.username;
            this.editableProfile.bio = this.profile.bio;
            this.editableProfile.profileImage = this.profile.profile_image || DefaultProfile;
            this.editableProfile.file = null;

            this.editMode = true;
        },

        // Cancel editing by reverting to original profile, hide form
        cancelEdit() {
            // Restore from current profile
            this.editableProfile.username = this.profile.username;
            this.editableProfile.bio = this.profile.bio;
            this.editableProfile.profileImage = this.profile.profile_image || DefaultProfile;
            this.editableProfile.file = null;

            this.editMode = false;
            this.error = null; // Clear any error messages
        }
    },
    watch: {
        profile: {
            handler(newProfile) {
                if (newProfile) {
                    // Keep editable data in sync if user isn't editing
                    if (!this.editMode) {
                        this.editableProfile.username = newProfile.username;
                        this.editableProfile.bio = newProfile.bio;
                        this.editableProfile.profileImage = newProfile.profile_image || DefaultProfile;
                    }
                }
            },
            deep: true,
        },
    },
};
</script>

<style scoped>
/* Existing read-only profile display */
.my-profile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--text-padding-300);
    max-width: 600px;
    margin: var(--text-padding-700) auto;
}

.my-profile-container img {
    object-fit: cover;
    width: 20rem;
    height: 20rem;
    border-radius: 100%;
    border: 2px solid var(--clr-primary-600);
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

.my-profile-container button {
    background-color: var(--clr-primary-600);
    color: var(--clr-neutral-0);
    font-size: var(--fs-button);
    font-weight: var(--fw-bold);
    border-radius: var(--default-border-radius);
    border: none;
    cursor: pointer;
    height: var(--default-btn-size);
    width: 50%;
    max-width: 15rem;
    margin-top: var(--text-padding-300);
}

/* Edit form (shown only if editMode == true) */
.profile-edit-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--text-padding-300);
    max-width: 600px;
    margin: var(--text-padding-700) auto;
}

.profile-edit-form .error-message {
    color: var(--clr-util-error);
    text-align: center;
    padding: var(--text-padding-300);
    margin: 0;
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
    min-height: 6rem;
    resize: vertical;
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
    width: 50%;
    max-width: 15rem;
}

/* Cancel button variation */
.profile-edit-form .cancel-btn {
    background-color: var(--clr-util-error);
    width: auto;
    padding: 0 1.2rem;
    margin-top: 0;
}
</style>