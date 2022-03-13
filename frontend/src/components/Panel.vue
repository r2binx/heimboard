<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { inject } from "vue"
import { NButton, NIcon, NLoadingBarProvider, NMessageProvider, NResult, NSpace } from "naive-ui"
import { PowerOff } from "@vicons/fa"
import Status from "@/components/Status.vue"
import SystemUsage from "@/components/SystemUsage.vue"
import NetworkUsage from "@/components/NetworkUsage.vue"
import Services from "@/components/Services.vue"
import KVM from "@/components/KVM.vue"
import Storage from "@/components/Storage.vue"
import { wakeOnLan } from "@/utils/api.js"
import { readableTime } from "@/utils/misc"

const auth = inject("auth")
const state = inject("state")

function handleWakeUp() {
	wakeOnLan()
		.then((res) => {
			if (res.data.success) {
				console.success("Woke up!")
			} else {
				console.error(res.data.message)
			}
		})
		.catch((err) => {
			console.error("Failed to wake up!")
			console.log(err)
		})
}

let scheduledBoot = $computed(() => readableTime(state.schedule.boot))
</script>

<template>
	<div v-if="auth.hasPermission('guest')">
		<div v-if="state.reachable">
			<n-message-provider>
				<Status />
			</n-message-provider>
			<SystemUsage />
			<NetworkUsage />
			<Services />
			<n-message-provider v-if="auth.hasPermission('admin')">
				<n-loading-bar-provider>
					<KVM />
				</n-loading-bar-provider>
			</n-message-provider>
			<Storage />
		</div>
		<div v-else>
			<n-space v-if="state.net_reachable" vertical justify="center">
				<p>Scheduled boot is at: {{ scheduledBoot }}</p>
				<br />
				<n-button style="font-size: 72px" circle :bordered="false" @click="handleWakeUp">
					<n-icon>
						<PowerOff />
					</n-icon>
				</n-button>
				<p style="font-size: large">WAKE UP</p>
			</n-space>
			<n-result
				v-else
				status="error"
				description="Seems like the network is unreachable"
			></n-result>
		</div>
	</div>
	<div v-else>
		<p>You haven't been authorized yet to view this page.</p>
	</div>
</template>
