<script setup lang="ts">
import { progressColor } from "@/utils/common";
import { NProgress, NSpace } from "naive-ui";
import { useWindowWidth } from "@/composables/useWindowWidth";

const { windowWidth } = useWindowWidth();

const props = defineProps<{ percentage: number; title: string }>();
</script>

<template>
    <n-progress
        type="circle"
        class="progress-circle"
        :color="progressColor(props.percentage)"
        :rail-color="progressColor(props.percentage, '33')"
        :stroke-width="8"
        :percentage="props.percentage"
        :style="{ width: windowWidth <= 420 ? '130px' : '150px' }"
    >
        <n-space vertical justify="center">
            <slot />
            <div>{{ props.title }}</div>
        </n-space>
    </n-progress>
</template>
