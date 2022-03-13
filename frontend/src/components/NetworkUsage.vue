<script setup>
import { inject, watchEffect } from "vue"
import { useWebSocket } from "@vueuse/core"
// import { $computed, $ref } from 'vue/macros'
import { NDivider, NSpace } from "naive-ui"
import ProgressCircle from "@/components/ProgressCircle.vue"

const auth = inject("auth")
const state = inject("state")

let upRate = $ref(0)
let netOutPct = $ref(0)

let downRate = $ref(0)
let netInPct = $ref(0)

let bandwidth = $computed(() => {
	let fritz = state.fritz
	return { in: ~~(fritz.net.down / 1e6), out: ~~(fritz.net.up / 1e6) }
})

watchEffect(async () => {
	const token = await auth.getToken()
	useWebSocket("wss://" + import.meta.env.VITE_APP_IDLEREPORTER + "/net?rate=1&token=" + token, {
		autoReconnect: true,
		onConnected: () => console.log("Successfully connected to the fritz websocket server..."),
		onMessage: (ws, event) => {
			let data = JSON.parse(event.data)
			downRate = ~~(data["in"] / 125000)
			upRate = ~~(data["out"] / 125000)

			netOutPct = (upRate / bandwidth.out) * 100
			netInPct = (downRate / bandwidth.in) * 100
		},
	})
})
</script>
<template>
	<n-divider title-placement="left">Network</n-divider>
	<n-space justify="space-around">
		<progress-circle :percentage="netInPct" title="IN"> {{ downRate }}Mbit/s </progress-circle>
		<progress-circle :percentage="netOutPct" title="OUT"> {{ upRate }}Mbit/s </progress-circle>
	</n-space>
</template>

<style></style>
