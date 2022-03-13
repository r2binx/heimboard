<script setup>
import { NProgress, NSpace } from "naive-ui"
import { progressColor } from "@/utils/misc.js"
import { inject } from "vue"

const windowWidth = inject("windowWidth")

const props = defineProps({
	percentage: Number,
	title: String,
})
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
			<div :style="{ fontSize: windowWidth <= 420 ? 'medium' : 'large' }">
				<slot></slot>
			</div>
			<div>{{ props.title }}</div>
		</n-space>
	</n-progress>
</template>
