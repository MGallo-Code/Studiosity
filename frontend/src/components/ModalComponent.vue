<template>
    <div class="modal" v-if="showModal">
        <div class="modal-content">
            <span class="close" @click="closeModal">&times;</span>
            <div v-if="modalError" class="error-message">{{ modalError }}</div>
            <slot></slot> <!-- This slot will be used to inject custom content -->
        </div>
    </div>
</template>

<script>
export default {
    props: {
        showModal: {
            type: Boolean,
            required: true
        },
        modalError: {
            type: String,
            default: ''
        }
    },
    methods: {
        closeModal() {
            this.$emit('update:showModal', false);
        }
    }
};
</script>

<style scoped>
.modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed; /* Stay in place */
    z-index: 1000; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0, 0, 0, 0.6); /* Black background with opacity */
}

.modal-content {
    background-color: #fff;
    margin: auto; /* Align to the center */
    padding: 20px;
    border: 1px solid #888;
    width: 50%; /* Adjust width for smaller screens if necessary */
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    animation-name: modalopen;
    animation-duration: 0.4s;
}

.error-message {
    color: #f44336;
    text-align: center;
    margin: 10px 0;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}

/* Add animation */
@keyframes modalopen {
    from {top: -300px; opacity: 0} 
    to {top: 0; opacity: 1}
}
</style>