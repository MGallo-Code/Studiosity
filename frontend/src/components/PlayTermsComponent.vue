<template>
    <div class="study-playlist-player">
        <div class="controls">
            <button @click="resetTermIndex">Back to Beginning</button>
            <button @click="previousTerm">Previous</button>
            <button @click="playPause">{{ isPlaying ? 'Pause' : 'Play' }}</button>
            <button @click="nextTerm">Next</button>
            <button @click="togglePlayOrder">{{ playFrontFirst ? 'Play Back First' : 'Play Front First' }}</button>
            <!-- <button @click="shuffleTerms">Shuffle</button> -->
        </div>

        <div class="sliders">
            <div>
                <label for="front-back-pause">Front/Back Pause: {{ frontBackPause }}s</label>
                <input type="range" id="front-back-pause" min="0" max="10" v-model="frontBackPause" />
            </div>
            <div>
                <label for="term-pause">Term Pause: {{ termPause }}s</label>
                <input type="range" id="term-pause" min="0" max="20" v-model="termPause" />
            </div>
        </div>

        <div class="loop-toggle">
            <input type="checkbox" id="loop" v-model="loop" />
            <label for="loop">Loop Playlist</label>
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
            currentTermIndex: 0,
            isPlaying: false,
            isFirstAudioNext: true,
            playFrontFirst: true,
            frontBackPause: 0.6,
            termPause: 1.2,
            loop: false,
            audioPlayer: null,
            nextTermTimeout: null,
            nextSideTimeout: null,
        };
    },
    mounted() {
        this.audioPlayer = new Audio();
        this.audioPlayer.addEventListener('ended', this.handleAudioEnd);
    },
    beforeUnmount() {
        this.audioPlayer.removeEventListener('ended', this.handleAudioEnd);
        this.audioPlayer = null;
    },
    computed: {
        currentTerm() {
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
                this.isFirstAudioNext = true;
                clearTimeout(this.nextTermTimeout);
                clearTimeout(this.nextSideTimeout);
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
            console.log('##' + this.isFirstAudioNext);
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
            if (this.currentTermIndex < this.studyTerms.length - 1) {
                this.currentTermIndex++;
            } else {
                this.currentTermIndex = 0;
                // Return early to avoid looping
                if (!this.loop) { return; }
            }
            this.isFirstAudioNext = true;
            this.playCurrentAudio();
        },
        previousTerm() {
            this.isPlaying = false;
            if (this.currentTermIndex > 0) {
                this.currentTermIndex--;
            } else if (this.loop) {
                this.currentTermIndex = this.studyTerms.length - 1;
            }
            this.isFirstAudioNext = true;
            this.isPlaying = true;
        },
        togglePlayOrder() {
            this.isPlaying = false;
            this.playFrontFirst = !this.playFrontFirst;
        },
        // shuffleTerms() {
        //     const shuffledTerms = this.shuffleArray([...this.studyTerms]);
        //     this.$emit('update:studyTerms', shuffledTerms);
        //     this.currentTermIndex = 0;
        //     this.refreshPlaying();
        // },
        // shuffleArray(array) {
        //     for (let i = array.length - 1; i > 0; i--) {
        //         const j = Math.floor(Math.random() * (i + 1));
        //         [array[i], array[j]] = [array[j], array[i]];
        //     }
        //     return array;
        // },
    }
};
</script>