<script setup>
import { inject, watchEffect } from "vue"
import { useWebSocket } from "@vueuse/core"
// import { $computed, $ref } from 'vue/macros'
import { NDivider, NSpace } from "naive-ui"
import ProgressCircle from "@/components/ProgressCircle.vue"

const auth = inject("auth")

let cpuUsage = $ref(0)
let memUsage = $ref(0)

watchEffect(async () => {
	const token = await auth.getToken()
	useWebSocket(
		"wss://" + import.meta.env.VITE_APP_IDLEREPORTER + "/usage?rate=1&token=" + token,
		{
			autoReconnect: true,
			onConnected: () =>
				console.log("Successfully connected to the system websocket server..."),
			onMessage: (ws, event) => {
				let data = JSON.parse(event.data)
				cpuUsage = data["cpu"]
				memUsage = data["memory"]["used"]
			},
		}
	)
})
</script>
<template>
	<n-divider title-placement="left">SYSTEM</n-divider>
	<n-space justify="space-around">
		<progress-circle :percentage="cpuUsage" title="CPU"> {{ ~~cpuUsage }}% </progress-circle>
		<progress-circle :percentage="memUsage" title="MEMORY"> {{ ~~memUsage }}% </progress-circle>
	</n-space>
</template>

<style></style>
