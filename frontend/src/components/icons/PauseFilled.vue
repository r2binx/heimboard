<script setup lang="ts">
import { NIcon } from "naive-ui";

// eslint-disable-next-line vue/no-setup-props-destructure
const { size, fillColor = "currentColor" } = defineProps<{
    size?: number;
    fillColor?: string;
}>();
</script>

<template>
    <n-icon :size="size">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 48 48"
        >
            <path
                d="M17.75 7A3.25 3.25 0 0 1 21 10.25v27.5A3.25 3.25 0 0 1 17.75 41h-5.5A3.25 3.25 0 0 1 9 37.75v-27.5A3.25 3.25 0 0 1 12.25 7h5.5zm18 0A3.25 3.25 0 0 1 39 10.25v27.5A3.25 3.25 0 0 1 35.75 41h-5.5A3.25 3.25 0 0 1 27 37.75v-27.5A3.25 3.25 0 0 1 30.25 7h5.5z"
                :fill="fillColor"
            ></path>
        </svg>
    </n-icon>
</template>
