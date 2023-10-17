<script setup lang="ts">
import type { JellyMediaState } from "@/types/ApiState";
import { timeToString } from "@/utils/common";
import { Pause, Play, Server } from "@vicons/fa";
import { computed, ref } from "vue";

const props = defineProps<{ details: Required<JellyMediaState> }>();

const stateIcon = computed(() => {
    return props.details.now_playing.paused ? Pause : Play;
});
const progressPercentage = computed(() => {
    return (
        (props.details.now_playing.position / props.details.now_playing.duration) * 100
    );
});

const timeLeft = computed(() => {
    const time = props.details.now_playing.duration - props.details.now_playing.position;
    return timeToString(time);
});

const toggleElapsed = ref(true);
</script>

<template>
    <n-thing content-indented>
        <template #avatar> <n-icon :component="stateIcon" /> </template>
        <template #header>
            <div style="font-size: 14px">{{ details.now_playing.title }}</div>
        </template>

        <template #description>
            <div style="font-size: 12px">
                {{ details.user }} on {{ details.client }} ({{ details.device }})
            </div></template
        >
        <template v-if="details.now_playing.play_method === 'Transcode'" #header-extra>
            <n-icon :component="Server" />
        </template>
        <div>
            <n-progress type="line" :percentage="Math.round(progressPercentage)">
                <span v-if="toggleElapsed" style="font-size: 12px">
                    {{ timeToString(details.now_playing.position) }} /
                    {{ timeToString(details.now_playing.duration) }}
                </span>
                <span v-else style="font-size: 12px">{{ timeLeft }} left</span>
            </n-progress>
        </div>
    </n-thing>
</template>
