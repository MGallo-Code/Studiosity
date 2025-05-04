<template>
    <!-- Modal overlay with dark, blurred background -->
    <div class="modal-overlay" @click.self="close">
        <!-- Overall modal close button -->
        <button class="modal-close" @click="close">
            <FontAwesomeIcon :icon="['fas', 'xmark']" />
        </button>
        <!-- Centered flashcard container -->
        <div class="flashcard-container">
            <div class="flashcard" :class="{ flipped: isFlipped, changing: isChangingCard }" @click="flipCard">
                <!-- Front face -->
                <div class="flashcard-face flashcard-front">
                    <img v-if="frontImage" :src="frontImage.file_path" class="flashcard-image" />
                    <p v-else>{{ frontContent }}</p>
                </div>
                <!-- Back face -->
                <div class="flashcard-face flashcard-back">
                    <img v-if="backImage" :src="backImage.file_path" class="flashcard-image" />
                    <p v-else>{{ backContent }}</p>
                </div>
            </div>
        </div>
        <!-- Bottom fixed menu -->
        <div class="bottom-menu" :class="{ collapsed: !menuExpanded }">
            <!-- Toggle button (only visible on small screens) -->
            <button class="menu-toggle" @click="toggleMenu">
                <FontAwesomeIcon :icon="menuExpanded ? ['fas', 'chevron-down'] : ['fas', 'chevron-up']" />
            </button>
            <!-- Menu content: on small screens, this is shown only when expanded;
             on larger screens (min-width:901px) it is always visible via CSS -->
            <div class="menu-content">
                <button class="menu-button" @click="prevCard">Previous</button>
                <button class="menu-button" @click="flipCard">Flip</button>
                <button class="menu-button" @click="nextCard">Next</button>
                <button class="menu-button" @click="toggleAutoPlay">
                    {{ autoPlay ? "Pause" : "Play" }}
                </button>
                <button class="menu-button" @click="toggleReverseSides">
                    {{ reverseSides ? "Normal Sides" : "Reverse Sides" }}
                </button>
                <button class="menu-button" @click="shuffleCards">
                    <FontAwesomeIcon :icon="['fas', 'shuffle']" />
                </button>
                <button class="menu-button" @click="toggleAdvancedSettings">
                    <FontAwesomeIcon :icon="['fas', 'gear']" />
                </button>
            </div>
        </div>
        <!-- Advanced Settings Panel - Now a Modal -->
        <div v-if="showAdvancedSettings" class="settings-modal-overlay" @click.self="toggleAdvancedSettings">
            <div class="advanced-settings">
                <!-- Advanced settings panel close button -->
                <button class="advanced-close" @click="toggleAdvancedSettings">
                    <FontAwesomeIcon :icon="['fas', 'xmark']" />
                </button>
                <div class="setting-item">
                    <label for="volume">Audio Volume: {{ playbackVolume }}</label>
                    <input id="volume" type="range" min="0" max="1" step="0.1" v-model.number="playbackVolume" />
                </div>
                <div class="setting-item">
                    <label for="speed">Playback Speed: {{ playbackRate }}x</label>
                    <input id="speed" type="range" min="0.1" max="3" step="0.1" v-model.number="playbackRate" />
                </div>
                <div class="setting-item">
                    <label for="frontBackPause">Pause Between Front/Back: {{ frontBackPause }}s</label>
                    <input id="frontBackPause" type="range" min="0" max="10" step="0.1" v-model.number="frontBackPause" />
                </div>
                <div class="setting-item">
                    <label for="termPause">Pause Between Terms: {{ termPause }}s</label>
                    <input id="termPause" type="range" min="0" max="20" step="0.1" v-model.number="termPause" />
                </div>
                <div class="setting-item">
                    <label for="noAudioPause">Pause Without Audio: {{ noAudioPause }}s</label>
                    <input id="noAudioPause" type="range" min="0" max="10" step="0.1" v-model.number="noAudioPause" />
                </div>
                <div class="setting-item">
                    <label for="pauseAfterAudio">Pause After Audio: {{ pauseAfterAudio }}s</label>
                    <input id="pauseAfterAudio" type="range" min="0" max="5" step="0.1" v-model.number="pauseAfterAudio" />
                </div>
                <div class="setting-item toggles">
                    <div class="toggle-control" @click="loop = !loop">
                        <label :class="{ 'active-toggle': loop, 'inactive-toggle': !loop }">
                            <FontAwesomeIcon :icon="['fas', 'repeat']" />
                        </label>
                        <span>Loop</span>
                    </div>
                    <div class="toggle-control" @click="shuffle = !shuffle">
                        <label :class="{ 'active-toggle': shuffle, 'inactive-toggle': !shuffle }">
                            <FontAwesomeIcon :icon="['fas', 'random']" />
                        </label>
                        <span>Shuffle</span>
                    </div>
                    <div class="toggle-control" @click="audioEnabled = !audioEnabled">
                        <label :class="{ 'active-toggle': audioEnabled, 'inactive-toggle': !audioEnabled }">
                            <FontAwesomeIcon :icon="['fas', 'volume-up']" />
                        </label>
                        <span>Audio</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, defineProps, defineEmits, nextTick } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
// Import additional icons and add them to the library
import { library } from '@fortawesome/fontawesome-svg-core';
import {
    faShuffle,
    faGear,
    faRepeat,
    faRandom,
    faVolumeUp,
    faXmark,
    faChevronUp,
    faChevronDown
} from '@fortawesome/free-solid-svg-icons';
library.add(faShuffle, faGear, faRepeat, faRandom, faVolumeUp, faXmark, faChevronUp, faChevronDown);

const props = defineProps({
    cards: { type: Array, required: true }
});
const emit = defineEmits(['close']);

// State variables
const currentIndex = ref(0);
const isFlipped = ref(false);
const autoPlay = ref(false);
const reverseSides = ref(false);
const showAdvancedSettings = ref(false);
const menuExpanded = ref(false); // state for bottom menu on small screens
const isChangingCard = ref(false); // Flag for inter-card transition

// Advanced settings
const playbackVolume = ref(1.0);
const playbackRate = ref(1.0);
const frontBackPause = ref(2.0);
const termPause = ref(2.0);
const loop = ref(false);
const shuffle = ref(false);
const audioEnabled = ref(true);
const noAudioPause = ref(1.0); // Pause duration when no audio is present
const pauseAfterAudio = ref(0.5); // Pause duration *after* audio finishes

// Audio player
const audioPlayer = ref(new Audio());
// Store current listeners to remove them later
const currentOnEndListener = ref(null);
const currentOnErrorListener = ref(null);

// Computed properties
const currentCard = computed(() => props.cards[currentIndex.value] || {});
const frontContent = computed(() =>
    currentCard.value
        ? reverseSides.value
            ? currentCard.value.back_text
            : currentCard.value.front_text
        : ''
);
const backContent = computed(() =>
    currentCard.value
        ? reverseSides.value
            ? currentCard.value.front_text
            : currentCard.value.back_text
        : ''
);
const frontImage = computed(() =>
    currentCard.value
        ? reverseSides.value
            ? currentCard.value.back_image
            : currentCard.value.front_image
        : null
);
const backImage = computed(() =>
    currentCard.value
        ? reverseSides.value
            ? currentCard.value.front_image
            : currentCard.value.back_image
        : null
);
const currentAudio = computed(() => {
    if (!currentCard.value) return null;
    return !isFlipped.value
        ? reverseSides.value
            ? currentCard.value.back_tts_audio
            : currentCard.value.front_tts_audio
        : reverseSides.value
            ? currentCard.value.front_tts_audio
            : currentCard.value.back_tts_audio;
});

// Auto play timer
let autoPlayTimer = null;
function clearAutoPlayTimer() {
    if (autoPlayTimer) {
        clearTimeout(autoPlayTimer);
        autoPlayTimer = null;
    }
    // Remove existing listeners
    if (currentOnEndListener.value) {
        audioPlayer.value?.removeEventListener('ended', currentOnEndListener.value);
        currentOnEndListener.value = null;
    }
    if (currentOnErrorListener.value) {
        audioPlayer.value?.removeEventListener('error', currentOnErrorListener.value);
        currentOnErrorListener.value = null;
    }
}
function scheduleNextAutoPlayAction() {
    if (!autoPlay.value) return;

    clearAutoPlayTimer(); // Ensure no old timers/listeners interfere

    const audioForThisFace = currentAudio.value;
    const shouldPlayAudio = audioEnabled.value && audioForThisFace;
    const nextAction = isFlipped.value ? nextCard : flipCard;

    if (shouldPlayAudio) {
        const onEnd = () => {
            removeAudioListeners(); // Ensure listeners are removed before setting timeout
            autoPlayTimer = setTimeout(nextAction, pauseAfterAudio.value * 1000);
        };
        const onError = () => {
            console.warn("Audio failed, using non-audio pause.");
            removeAudioListeners();
            const fallbackPause = isFlipped.value ? termPause.value : frontBackPause.value;
            autoPlayTimer = setTimeout(nextAction, fallbackPause * 1000);
        };

        // Store listeners so they can be removed by clearAutoPlayTimer
        currentOnEndListener.value = onEnd;
        currentOnErrorListener.value = onError;

        // Add one-time listeners
        audioPlayer.value.addEventListener('ended', onEnd, { once: true });
        audioPlayer.value.addEventListener('error', onError, { once: true });

        // Set source, volume, rate and play
        audioPlayer.value.src = audioForThisFace.file_path;
        audioPlayer.value.volume = playbackVolume.value;
        audioPlayer.value.playbackRate = playbackRate.value;
        audioPlayer.value.play().catch(err => {
            console.error("Audio play error on initial call:", err);
            onError(); // Trigger error handling path if play() fails immediately
        });

    } else {
        // No audio: use standard non-audio pause
        const pauseDuration = isFlipped.value ? termPause.value : frontBackPause.value;
        autoPlayTimer = setTimeout(nextAction, pauseDuration * 1000);
    }
}

// Helper to remove listeners inside the listeners themselves if needed
function removeAudioListeners() {
    if (currentOnEndListener.value) {
        audioPlayer.value?.removeEventListener('ended', currentOnEndListener.value);
        currentOnEndListener.value = null;
    }
    if (currentOnErrorListener.value) {
        audioPlayer.value?.removeEventListener('error', currentOnErrorListener.value);
        currentOnErrorListener.value = null;
    }
}

function flipCard() {
    isFlipped.value = !isFlipped.value;
    // If autoplay is on, schedule the next action (next card or flip back)
    if (autoPlay.value) {
        scheduleNextAutoPlayAction();
    }
}

function nextCard() {
    clearAutoPlayTimer(); // Stop pending actions before manual navigation
    if (props.cards.length <= 1) {
        autoPlay.value = false;
        return;
    }

    let nextIndex;
    if (shuffle.value) {
        do {
            nextIndex = Math.floor(Math.random() * props.cards.length);
        } while (props.cards.length > 1 && nextIndex === currentIndex.value);
    } else {
        if (currentIndex.value < props.cards.length - 1) {
            nextIndex = currentIndex.value + 1;
        } else {
            if (loop.value) {
                nextIndex = 0;
            } else {
                autoPlay.value = false;
                return;
            }
        }
    }

    isChangingCard.value = true; // Activate transition state
    isFlipped.value = false;     // Ensure front face is target state

    setTimeout(() => {
        currentIndex.value = nextIndex; // Update content *after* flip back starts

        // Use nextTick ensures the DOM has the new content before resetting transition state
        nextTick(() => {
            isChangingCard.value = false; // Deactivate transition state
            if (autoPlay.value) {
                scheduleNextAutoPlayAction(); // Schedule based on the new card's front face
            }
        });
    }, 100); // Increased timeout to allow CSS hide transition more time
}

function prevCard() {
    clearAutoPlayTimer(); // Stop pending actions before manual navigation
    let prevIndex;
    if (currentIndex.value > 0) {
        prevIndex = currentIndex.value - 1;
    } else {
        prevIndex = props.cards.length - 1; // Wrap around
    }

    isChangingCard.value = true; // Activate transition state
    isFlipped.value = false;     // Ensure front face is target state

    setTimeout(() => {
        currentIndex.value = prevIndex; // Update content *after* flip back starts

        nextTick(() => {
            isChangingCard.value = false; // Deactivate transition state
            if (autoPlay.value) {
                scheduleNextAutoPlayAction(); // Schedule based on the new card's front face
            }
        });
    }, 100);
}

function toggleAutoPlay() {
    autoPlay.value = !autoPlay.value;
    if (autoPlay.value) {
        // Start the cycle
        scheduleNextAutoPlayAction();
    } else {
        // Stop the cycle
        clearAutoPlayTimer();
    }
}

function toggleReverseSides() {
    reverseSides.value = !reverseSides.value;
    isFlipped.value = false;
    // Reschedule if autoplay is on, as content has changed
    if (autoPlay.value) {
        scheduleNextAutoPlayAction();
    }
}

function shuffleCards() {
    clearAutoPlayTimer();
    shuffle.value = !shuffle.value;
    let newIndex = currentIndex.value; // Default to current if only 1 card
    if (props.cards.length > 1) {
        do {
            newIndex = Math.floor(Math.random() * props.cards.length);
        } while (newIndex === currentIndex.value);
    }

    isChangingCard.value = true; // Activate transition state
    isFlipped.value = false;     // Ensure front face is target state

    setTimeout(() => {
        currentIndex.value = newIndex; // Update content *after* flip back starts

        nextTick(() => {
            isChangingCard.value = false; // Deactivate transition state
            if (autoPlay.value) {
                scheduleNextAutoPlayAction(); // Schedule based on the new card's front face
            }
        });
    }, 100);
}

function toggleAdvancedSettings() {
    showAdvancedSettings.value = !showAdvancedSettings.value;
}
function toggleMenu() {
    menuExpanded.value = !menuExpanded.value;
}
function close() {
    clearAutoPlayTimer();
    emit("close");
}
onBeforeUnmount(() => {
    clearAutoPlayTimer();
    audioPlayer.value = null;
});
</script>

<style scoped>
/* Use theme variables from base-style.css */

/* Modal overlay with dark, blurred background */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

/* Overall modal close button (top right) */
.modal-close {
    position: absolute;
    top: var(--text-padding-300);
    right: var(--text-padding-300);
    background-color: var(--clr-util-error);
    color: var(--clr-neutral-0);
    border: none;
    border-radius: var(--default-border-radius);
    width: var(--default-btn-size);
    height: var(--default-btn-size);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    z-index: 1200;
}

/* Flashcard container for large screens */
.flashcard-container {
    width: 75%;
    max-width: 60%;
    padding: var(--text-padding-400);
    margin-bottom: 120px;
}

/* Flashcard styling */
.flashcard {
    width: 100%;
    height: 65vh;
    perspective: 1000px;
    position: relative;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    cursor: pointer;
    border: 2rem solid var(--clr-neutral-0);
    border-radius: var(--default-border-radius);
    background-color: var(--clr-neutral-0);
}

.flashcard.flipped {
    transform: rotateY(180deg);
}

.flashcard-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: var(--default-border-radius);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding: var(--text-padding-400);
    font-size: var(--fs-600);
    background: var(--clr-neutral-0);
}

.flashcard-back {
    transform: rotateY(180deg);
}

.flashcard-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.bottom-menu {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  /* Remove fixed height so it adapts to content */
  /* height: calc(4rem + var(--default-border-radius) * 2 + 4 * var(--text-padding-250)); */
  background: var(--clr-neutral-50);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.3);
  /* Reduce vertical and horizontal padding */
  padding: var(--text-padding-200) var(--text-padding-300);
  display: flex;
  /* Use a gap instead of space-around if you need more control */
  gap: var(--text-padding-250);
  align-items: center;
  justify-content: center;  /* or 'space-between' if you want to spread them out evenly */
  z-index: 1100;
  transition: transform 0.3s;
}

/* Menu toggle button (visible on small screens) */
.menu-toggle {
    background-color: var(--clr-primary-600);
    color: var(--clr-neutral-0);
    height: 4rem;
    border: none;
    border-radius: var(--default-border-radius);
    padding: var(--text-padding-250);
    cursor: pointer;
    font-size: var(--fs-400);
}

/* Style for the other menu buttons */
.menu-button {
    flex-grow: 1;
    background-color: var(--clr-primary-700);
    color: var(--clr-neutral-0);
    height: 4rem;
    border: none;
    border-radius: var(--default-border-radius);
    padding: var(--text-padding-400) var(--text-padding-500);
    cursor: pointer;
    font-size: var(--fs-400);
    min-width: 100px;
    margin: 0.2rem;
    transition: var(--default-transition);
}

.menu-button:hover {
    background-color: var(--clr-primary-800);
}

/* When the menu is collapsed on small screens, only show the toggle */
.bottom-menu.collapsed .menu-content {
    display: none;
}



/* Bottom menu content container */
.menu-content {
    display: flex;
    flex-direction: column;
    gap: var(--text-padding-250);
    width: 100%;
}

/* Advanced Settings Panel */
.settings-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(3px); /* Optional: adds blur to background */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1300; /* Ensure it's above everything else */
}

.advanced-settings {
    /* Now the modal content box */
    position: relative; /* For positioning the close button */
    background-color: var(--clr-neutral-0);
    padding: var(--text-padding-850) var(--text-padding-800);
    padding-top: var(--text-padding-1000); /* More space at top for close button */
    border-radius: var(--default-border-radius);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    gap: var(--text-padding-250);
    width: 90%; /* Responsive width */
    max-width: 500px; /* Max width on larger screens */
}

.advanced-close {
    position: absolute;
    top: var(--text-padding-300); /* Position inside the modal */
    right: var(--text-padding-300);
    background-color: var(--clr-util-error);
    color: var(--clr-neutral-0);
    border: none;
    border-radius: var(--default-border-radius);
    width: var(--default-btn-size);
    height: var(--default-btn-size);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    z-index: 1200;
}

.setting-item {
    display: flex;
    flex-direction: column;
    font-size: var(--fs-300);
}

.setting-item input[type="range"] {
    width: 100%;
}

.toggles {
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.toggle-control {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

.toggle-control label {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    border: 2px solid;
    margin-bottom: 0.25rem;
    transition: var(--default-transition);
    font-size: var(--fs-400);
}

.toggle-control label.active-toggle {
    color: var(--clr-util-success);
    border-color: var(--clr-util-success);
}

.toggle-control label.inactive-toggle {
    color: var(--clr-util-error);
    border-color: var(--clr-util-error);
}

/* For smaller screens, allow the container to expand */
@media (max-width: 950px) {
    .flashcard-container {
        width: 95%;
    }

    .flashcard {
        height: 60vh;
    }
}

/* On small screens, the menu becomes a column with the toggle visible */
@media (max-width: 950px) {
    .bottom-menu {
        flex-direction: column;
        gap: var(--text-padding-250);
        padding: var(--text-padding-250);
    }

    .bottom-menu button {
        width: 100%;
    }

    .advanced-settings {
        /* Modal styling handles responsiveness, remove specific mobile overrides */
        /* bottom: 110px; */
        /* padding: var(--text-padding-250); */
    }

    /* Ensure the toggle button is visible */
    .menu-toggle {
        display: block;
    }
}

/* On larger screens the menu is always expanded and the toggle is hidden */
@media (min-width: 951px) {
    .menu-toggle {
        display: none;
    }

    .menu-content {
        display: flex !important;
        flex-direction: row;
        gap: var(--text-padding-250);
    }
}

.flashcard.changing .flashcard-back {
    backface-visibility: hidden; /* Reinforce */
    visibility: hidden;          /* Hide during content swap */
    opacity: 0;
    transition: opacity 0.05s ease-out, visibility 0.05s ease-out; /* Quick hide transition */
}
</style>