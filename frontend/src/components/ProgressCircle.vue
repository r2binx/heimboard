<script setup>
import { NProgress, NSpace } from 'naive-ui'
import { progressColor } from '../utils/misc.js'

const props = defineProps({
    percentage: Number,
    title: String,
})


</script>
<template>
    <n-progress
        type="circle"
        :color="progressColor(props.percentage)"
        :rail-color="progressColor(props.percentage, '33')"
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