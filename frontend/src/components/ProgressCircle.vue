<script setup>
import { NSpace, NProgress } from 'naive-ui'

const props = defineProps({
    percentage: Number,
    title: String,
})

function circleColor(value, alpha = 'FF') {
    if (value < 25) {
        return '#87D4F9' + alpha;
    } else if (value >= 25 && value < 40) {
        return '#61DBC3' + alpha;
    } else if (value >= 40 && value < 70) {
        return '#95DA74' + alpha;
    } else if (value >= 70 && value < 90) {
        return '#FAD375' + alpha;
    } else {
        return '#D9534F' + alpha;
    }
}
</script>
<template>
    <n-progress
        type="circle"
        :color="circleColor(props.percentage)"
        :rail-color="circleColor(props.percentage, '33')"
        :stroke-width="8"
        :percentage="props.percentage"
        style="width: 150px; "
    >
        <n-space vertical justify="center">
            <div style="font-size: large">
                <slot></slot>
            </div>
            <div>{{ props.title }}</div>
        </n-space>
    </n-progress>
</template>