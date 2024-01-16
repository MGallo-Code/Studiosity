<template>
    <div class="study-playlist-player">
        <div class="term-play-display">
            <button @click="previousTerm"><font-awesome-icon :icon="['fas', 'arrow-left']" /></button>
            <span>
                <p v-if="(isFirstAudioNext && playFrontFirst) || (!isFirstAudioNext && !playFrontFirst)">{{
                    currentTerm.front_text }}</p>
                <p v-else>{{ currentTerm.back_text }}</p>
                <button @click="playPause">
                    <font-awesome-icon v-if="isPlaying" :icon="['fas', 'pause']" />
                    <font-awesome-icon v-else :icon="['fas', 'play']" />
                </button>
            </span>
            <button @click="nextTerm"><font-awesome-icon :icon="['fas', 'arrow-right']" /></button>
        </div>

        <div class="term-play-controls">
            <button @click="resetTermIndex">Back to Beginning</button>
            <button @click="togglePlayOrder">{{ playFrontFirst ? 'Play Back First' : 'Play Front First' }}</button>
            <button @click="shuffleTerms">Re-Shuffle Terms</button>
        </div>

        <div class="term-play-sliders">
            <div>
                <label for="front-back-pause">Front/Back Pause: {{ frontBackPause }}s</label>
                <input type="range" id="front-back-pause" min="0" max="10" step="0.1" v-model="frontBackPause" />
            </div>
            <div>
                <label for="term-pause">Term Pause: {{ termPause }}s</label>
                <input type="range" id="term-pause" min="0" max="20" step="0.1" v-model="termPause" />
            </div>
        </div>

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
            isFirstAudioNext: true,
            playFrontFirst: true,
            frontBackPause: 0.6,
            termPause: 1.2,
            loop: false,
            shuffle: false,
            audioPlayer: null,
            nextTermTimeout: null,
            nextSideTimeout: null,
        };
    },
    mounted() {
        this.audioPlayer = new Audio();
        this.audioPlayer.addEventListener('ended', this.handleAudioEnd);
        // Shuffle terms
        this.shuffleTerms();
    },
    beforeUnmount() {
        this.audioPlayer.removeEventListener('ended', this.handleAudioEnd);
        this.audioPlayer = null;
    },
    computed: {
        currentTerm() {
            if (this.shuffle) {
                return this.shuffledTerms[this.currentTermIndex];
            }
            return this.studyTerms[this.currentTermIndex];
        },
        currentAudio() {
            const term = this.currentTerm;
            if ((this.isFirstAudioNext && this.playFrontFirst) || (!this.isFirstAudioNext && !this.playFrontFirst)) {
                return term.front_audio || term.front_tts_audio;
            } else {
                return term.back_audio || term.back_tts_audio;
            }
        }
    },
    watch: {
        isPlaying(newValue) {
            if (newValue) {
                this.playCurrentAudio();
            } else {
                this.audioPlayer.pause();
                clearTimeout(this.nextTermTimeout);
                clearTimeout(this.nextSideTimeout);
            }
        },
        shuffle(newValue) {
            if (newValue) {
                this.shuffleTerms();
            }
        }
    },
    methods: {
        resetTermIndex() {
            this.isPlaying = false;
            this.currentTermIndex = 0;
        },
        playPause() {
            this.isPlaying = !this.isPlaying;
        },
        playCurrentAudio() {
            if (this.currentAudio) {
                this.audioPlayer.src = this.currentAudio.file_path;
                this.audioPlayer.play().catch(error => console.error("Error playing audio:", error));
            }
        },
        handleAudioEnd() {
            if (!this.isFirstAudioNext) {
                this.nextTermTimeout = setTimeout(this.nextTerm, 1000 * this.termPause);
            } else {
                this.nextSideTimeout = setTimeout(this.playCurrentAudio, 1000 * this.frontBackPause);
            }
            this.isFirstAudioNext = !this.isFirstAudioNext;
        },
        nextTerm() {
            const wasPlaying = this.isPlaying;
            if (this.currentTermIndex < this.studyTerms.length - 1) {
                this.currentTermIndex++;
            } else {
                if (this.shuffle) {
                    this.shuffleTerms();
                }
                this.currentTermIndex = 0;
                // Return early to avoid looping
                if (!this.loop) {
                    this.isPlaying = false;
                    return;
                }
            }
            this.isFirstAudioNext = true;
            this.isPlaying = wasPlaying;
            if (this.isPlaying) this.playCurrentAudio();
        },
        previousTerm() {
            const wasPlaying = this.isPlaying;
            if (this.currentTermIndex > 0) {
                this.currentTermIndex--;
            } else if (this.loop) {
                this.currentTermIndex = this.studyTerms.length - 1;
            }
            this.isFirstAudioNext = true;
            this.isPlaying = wasPlaying;
        },
        togglePlayOrder() {
            this.isPlaying = false;
            this.playFrontFirst = !this.playFrontFirst;
        },
        shuffleTerms() {
            this.isPlaying = false;
            this.shuffledTerms = this.shuffleArray([...this.studyTerms]);
            this.currentTermIndex = 0;
            this.isFirstAudioNext = true;
        },
        shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = i === 1 ? 0 : Math.floor(Math.random() * i);

                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }
    }
};
</script>

<style scoped>
/* Shuffle and repeat toggle buttons(/labels) */
.study-playlist-player label.active-toggle {
    color: var(--clr-btn-green);
}

.study-playlist-player label.inactive-toggle {
    color: #9d5353;
}

.study-playlist-player label.active-toggle,
.study-playlist-player label.inactive-toggle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background-color: white;
    border: 2px solid var(--clr-base-primary);
    border-radius: 15px;
}

.study-playlist-player label.active-toggle:hover,
.study-playlist-player label.inactive-toggle:hover {
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.15);
}
</style>