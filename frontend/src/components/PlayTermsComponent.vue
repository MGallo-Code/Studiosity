<template>
    <div class="study-playlist-player">
        <div class="term-play-display">
            <button @click="previousTerm" class="term-play-side-btn"><font-awesome-icon
                    :icon="['fas', 'arrow-left']" /></button>
            <span @click="playPause" style="cursor:pointer;">
                <p>{{ currentText }}</p>
                <div class="play-pause-btn">
                    <font-awesome-icon v-if="isPlaying" :icon="['fas', 'pause']" />
                    <font-awesome-icon v-else :icon="['fas', 'play']" />
                </div>
            </span>
            <button @click="nextTerm" class="term-play-side-btn"><font-awesome-icon
                    :icon="['fas', 'arrow-right']" /></button>
        </div>

        <div class="term-play-controls">
            <button @click="resetTermIndex">Back to Beginning</button>
            <button @click="togglePlayOrder">{{ playFrontFirst ? 'Play Back First' : 'Play Front First' }}</button>
            <button @click="shuffleTerms">Re-Shuffle Terms</button>
            <div class="loop-toggle">
                <input type="checkbox" id="loop" v-model="loop" style="display:none;" />
                <label for="loop" :class="{ 'active-toggle': loop, 'inactive-toggle': !loop }"><font-awesome-icon
                        :icon="['fas', 'repeat']" /></label>
            </div>
            <div class="shuffle-toggle">
                <input type="checkbox" id="shuffle" v-model="shuffle" style="display:none;" />
                <label for="shuffle" :class="{ 'active-toggle': shuffle, 'inactive-toggle': !shuffle }"><font-awesome-icon
                        :icon="['fas', 'shuffle']" /></label>
            </div>
            <div class="audio-menu-toggle">
                <input type="checkbox" id="audio-menu-toggle" v-model="showingAudioMenu" style="display:none;" />
                <label for="audio-menu-toggle"
                    :class="{ 'menu-active': showingAudioMenu, 'menu-inactive': !showingAudioMenu }">
                    <font-awesome-icon v-if="showingAudioMenu" :icon="['fas', 'xmark']" />
                    <font-awesome-icon v-else :icon="['fas', 'gear']" /></label>
            </div>
        </div>

        <div v-if="showingAudioMenu" class="term-play-sliders">
            <div>
                <label for="playback-volume">Audio Volume: {{ playbackVolume }}</label>
                <input type="range" id="playback-volume" min="0" max="1" step="0.1" v-model="playbackVolume" />
            </div>
            <div>
                <label for="playback-rate">Audio Playback Speed: {{ playbackRate }}x</label>
                <input type="range" id="playback-rate" min="0.1" max="3" step="0.1" v-model="playbackRate" />
            </div>
            <div>
                <label for="front-back-pause">Pause Between Front/Back: {{ frontBackPause }}s</label>
                <input type="range" id="front-back-pause" min="0" max="10" step="0.1" v-model="frontBackPause" />
            </div>
            <div>
                <label for="term-pause">Pause Between Terms: {{ termPause }}s</label>
                <input type="range" id="term-pause" min="0" max="20" step="0.1" v-model="termPause" />
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    name: 'PlayTermsComponent',
    props: {
        studyTerms: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            shuffledTerms: null,
            currentTermIndex: 0,
            isPlaying: false,
            currentSide: 'front', // Either 'front' or 'back' 
            playFrontFirst: true,
            playbackVolume: 1.0,
            playbackRate: 1.0,
            frontBackPause: 0.6,
            termPause: 1.2,
            loop: false,
            shuffle: false,
            audioPlayer: new Audio(),
            nextTermTimeout: null,
            nextSideTimeout: null,
            showingAudioMenu: false
        };
    },
    mounted() {
        this.audioPlayer.addEventListener('ended', this.handleAudioEnd);
        // Shuffle terms
        this.shuffleTerms();
        window.addEventListener('keydown', this.handleKeyPress);
    },
    beforeUnmount() {
        this.audioPlayer.removeEventListener('ended', this.handleAudioEnd);
        this.audioPlayer = null;
        window.removeEventListener('keydown', this.handleKeyPress);
    },
    computed: {
        // Return our term at currentTermIndex based on whether shuffle is enabled
        currentTerm() {
            return this.shuffle ? this.shuffledTerms[this.currentTermIndex] : this.studyTerms[this.currentTermIndex];
        },
        // Get the audio for the current term
        currentAudio() {
            const term = this.currentTerm;
            // If we're playing audio from the card's front side
            if ((this.currentSide === 'front' && this.playFrontFirst)
                || (this.currentSide === 'back' && !this.playFrontFirst)) {
                return term.front_audio || term.front_tts_audio;
            }
            // If we're playing audio from the card's back side
            else {
                return term.back_audio || term.back_tts_audio;
            }
        },
        // Similarly, get the text for the current side of the card
        currentText() {
            const term = this.currentTerm;
            if ((this.currentSide === 'front' && this.playFrontFirst)
                || (this.currentSide === 'back' && !this.playFrontFirst)) {
                return term.front_text;
            } else {
                return term.back_text;
            }
        }
    },
    watch: {
        playbackVolume(volume) {
            this.audioPlayer.volume = volume;
        },
        playbackRate(rate) {
            this.audioPlayer.playbackRate = rate;
        },
        shuffle(newValue) {
            if (newValue) {
                this.shuffleTerms();
                // Make sure that shuffle is enabled...
                this.shuffle = true;
            }
        }
    },
    methods: {
        playPause() {
            this.isPlaying = !this.isPlaying;
            // If we're pausing...
            if (!this.isPlaying) {
                this.audioPlayer.pause();
                clearTimeout(this.nextTermTimeout);
                clearTimeout(this.nextSideTimeout);
            }
            // If we're playing...
            else {
                this.playCurrentAudio();
            }
        },
        playCurrentAudio() {
            if (this.currentAudio) {
                this.audioPlayer.src = this.currentAudio.file_path;
                this.audioPlayer.volume = Number(this.playbackVolume);
                this.audioPlayer.playbackRate = this.playbackRate;
                this.audioPlayer.play().catch(error => console.error("Error playing audio:", error));
            }
        },
        handleAudioEnd() {
            // Clear any extra coroutines...
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            this.audioPlayer.pause();

            // If we just played back side of card
            if (this.currentSide === 'back') {
                // Switch to next term in this.termPause seconds
                this.nextTermTimeout = setTimeout(this.nextTerm, 1000 * this.termPause);
            } else {
                // Flip card side in this.frontBackPause seconds
                this.nextSideTimeout = setTimeout(this.nextSide, 1000 * this.frontBackPause);
            }
        },
        nextTerm() {
            // Clear timeouts to prevent unintended behavior when manually navigating terms
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            this.audioPlayer.pause();

            // If not at the end of list, freely increase our currentTermIndex
            if (this.currentTermIndex < this.studyTerms.length - 1) {
                this.currentTermIndex++;
            }
            // If on the last element...
            else {
                // Reset currentTermIndex to beginning of list
                this.currentTermIndex = 0;
                // If shuffle is enabled, reshuffle the list since end has been reached
                if (this.shuffle) {
                    this.shuffleTerms();
                }
                // Return early to avoid looping if loop is not enabled
                if (!this.loop) {
                    this.isPlaying = false;
                    return;
                }
            }
            // Reset currentSide to be the front side
            this.currentSide = 'front';
            // Only play audio if player is actively in the playing state...
            if (this.isPlaying) this.playCurrentAudio();
        },
        nextSide() {
            // Clear timeouts to prevent unintended behavior when manually navigating terms
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            this.audioPlayer.pause();

            // Flip card side
            this.currentSide = this.currentSide === 'front' ? 'back' : 'front';
            // Play audio
            this.playCurrentAudio();
        },
        previousTerm() {
            // Clear timeouts to prevent unintended behavior when manually navigating terms
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            this.audioPlayer.pause();

            // If not the first term, simply decrease our term index
            if (this.currentTermIndex > 0) {
                this.currentTermIndex--;
            }
            // If the first term, set index to the end of list
            else {
                this.currentTermIndex = this.studyTerms.length - 1;
            }
            // Reset currentSide to be the front side
            this.currentSide = 'front';
            // Only play audio if player is actively in the playing state...
            if (this.isPlaying) this.playCurrentAudio();
        },
        resetTermIndex() {
            // Clear timeouts to prevent unintended behavior
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            this.audioPlayer.pause();
            // Reset our currentTermIndex
            this.currentTermIndex = 0;
        },
        togglePlayOrder() {
            // Clear timeouts to prevent unintended behavior
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            // Pause if currently playing
            if (this.isPlaying) {
                this.playPause();
            }

            // Change play order
            this.playFrontFirst = !this.playFrontFirst;

            // Reset currentSide to be the front side
            this.currentSide = 'front';
        },
        shuffleTerms() {
            // Clear timeouts to prevent unintended behavior
            clearTimeout(this.nextTermTimeout);
            clearTimeout(this.nextSideTimeout);
            // Pause if currently playing, reset to card front
            if (this.isPlaying) {
                this.playPause();
                this.currentSide = 'front';
            }

            // Shuffle!
            this.shuffledTerms = this.shuffleArray([...this.studyTerms]);

            // Reset currentSide based on playFrontFirst
            this.currentSide = this.playFrontFirst ? 'front' : 'back';
            // Reset term index
            this.currentTermIndex = 0;
        },
        shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = i === 1 ? 0 : Math.floor(Math.random() * i);

                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        },
        handleKeyPress(event) {
            switch (event.keyCode) {
                case 32: // Spacebar
                    event.preventDefault(); // Prevent the default action (scrolling)
                    this.playPause();
                    break;
                case 37: // Left arrow
                    this.previousTerm();
                    break;
                case 39: // Right arrow
                    this.nextTerm();
                    break;
            }
        }
    }
};
</script>

<style scoped>
.study-playlist-player {
    background-color: lightgray;
    border: 1px solid #a2a2a2;
}

.term-play-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 8rem;
    margin-bottom: 0.4rem;
    background-color: #f5f5f5;
    border-bottom: 1px solid #a2a2a2;
}

/* Prev/Next Term Buttons */

.term-play-side-btn {
    flex: 0 0 3rem;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0 !important;
    border: none !important;
}

/* Main term display area */

.term-play-display>span {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}

/* Text in term display area */
.term-play-display>span>p {
    flex: 1 0 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    padding: 0.8rem 5%;
}

.play-pause-btn {
    flex: 0 0 2rem;
}

/* Play Terms Controls Button Container */

.term-play-controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.4rem;
    padding: 0 .4rem .4rem .4rem;
    margin: 0 auto;
}

/* Buttons in Play Terms Controls */

.term-play-controls button {
    flex: 0 0 auto;
    white-space: nowrap;
    background-color: #f5f5f5;
    border: 1px solid #a2a2a2;
    height: 2.5rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 8px;
}

/* Shuffle and repeat toggle buttons(/labels) */

.loop-toggle,
.shuffle-toggle {
    display: inline-block;
}

.study-playlist-player label.active-toggle {
    color: var(--clr-btn-green);
    border: 2px solid var(--clr-btn-green);
}

.study-playlist-player label.inactive-toggle {
    color: #9d5353;
    border: 2px solid #9d5353;
}

.study-playlist-player label.active-toggle,
.study-playlist-player label.inactive-toggle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background-color: #f5f5f5;
    border-radius: 11px;
}

.study-playlist-player label.active-toggle:hover,
.study-playlist-player label.inactive-toggle:hover {
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.15);
}

/* Slider menu container */
.term-play-sliders {
    padding: 0 1rem;
}

/* Slider menu toggle */
.audio-menu-toggle label {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background-color: #f5f5f5;
    border-radius: 11px;
    cursor: pointer;
}

.audio-menu-toggle label:hover {
    background-color: #f5f5f5;
    border: 2px solid black;
}

/* Sliders + Slider Labels */

.term-play-sliders input[type="range"] {
    width: 100%;
    margin-bottom: 1rem;
}
</style>