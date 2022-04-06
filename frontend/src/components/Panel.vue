<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { inject } from "vue"
import {
	NButton,
	NIcon,
	NLoadingBarProvider,
	NMessageProvider,
	NResult,
	NSpace,
	useLoadingBar,
	useMessage,
} from "naive-ui"
import { PowerOff } from "@vicons/fa"
import Status from "@/components/Status.vue"
import SystemUsage from "@/components/SystemUsage.vue"
import NetworkUsage from "@/components/NetworkUsage.vue"
import Services from "@/components/Services.vue"
import KVM from "@/components/KVM.vue"
import Storage from "@/components/Storage.vue"
import { wakeOnLan } from "@/utils/api.js"
import BootTimePicker from "./BootTimePicker.vue"

const auth = inject("auth")
const state = inject("state")
const loadingBar = useLoadingBar()
const message = useMessage()

function handleWakeUp() {
	loadingBar.start()
	wakeOnLan()
		.then((res) => {
			if (res.data.success) {
				loadingBar.finish()
				message.success("Wake up successful, please wait for services to come online")
				setTimeout(state.refreshState, 2000)
			} else {
				console.error(res.data.message)
				loadingBar.error()
				message.error("Wake up failed")
			}
		})
		.catch((err) => {
			loadingBar.error()
			console.error("Failed to wake up!")
			console.log(err)
		})
}
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
		<template v-else>
			<n-space v-if="state.net_reachable" vertical justify="center">
				<n-space style="margin-bottom: 25px; align-items: center" justify="center">
					<p>Scheduled boot is at:</p>
					<BootTimePicker />
				</n-space>
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
		</template>
	</div>
	<div v-else>
		<p>You haven't been authorized yet to view this page.</p>
	</div>
</template>
