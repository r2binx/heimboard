<script setup>
import { inject } from "vue"
// import { $ref } from 'vue/macros'
import { NButton, NIcon, NPopconfirm, NSpace, NThing, useLoadingBar, useMessage } from "naive-ui"
import Pause from "@/assets/Pause.svg"
import RefreshOutlined from "@/assets/RefreshOutlined.svg"
import { Desktop, PowerOff, Skull } from "@vicons/fa"
import { destroyVm, resumeVm, startVm, stopVm, suspendVm } from "@/utils/api"
import MemorySlider from "@/components/MemorySlider.vue"
import MemoryDropdown from "@/components/MemoryDropdown.vue"

const message = useMessage()
const loadingBar = useLoadingBar()
const windowWidth = inject("windowWidth")

const props = defineProps({
	vm: Object,
})

const state = inject("state")
let buttonLoading = $ref({})

function handleVmStart(name) {
	loadingBar.start()
	buttonLoading[name] = true
	startVm(name)
		.then((res) => {
			if (res.data.result.success) {
				message.success("Successfully started " + name)
				loadingBar.finish()
				state.refreshState()
			} else {
				message.error(res.data.result.message)
				loadingBar.error()
			}
			buttonLoading[name] = false
		})
		.catch((err) => {
			message.error("Failed to start " + name)
			loadingBar.error()
			buttonLoading[name] = false
			console.log(err)
		})
}

function confirmShutdown(name) {
	loadingBar.start()
	buttonLoading[name] = true
	stopVm(name)
		.then((res) => {
			if (res.data.result.success) {
				message.success("Shutdown successful " + name)
				loadingBar.finish()
				state.refreshState()
			} else {
				message.error(res.data.result.message)
				loadingBar.error()
			}
			buttonLoading[name] = false
		})
		.catch((err) => {
			message.error("Failed to shutdown " + name)
			console.log(err)
			buttonLoading[name] = false
			loadingBar.error()
		})
}

function confirmSuspend(name) {
	loadingBar.start()
	buttonLoading[name] = true
	suspendVm(name)
		.then((res) => {
			if (res.data.result.success) {
				message.success("Suspending successful " + name)
				loadingBar.finish()
				state.refreshState()
			} else {
				message.error(res.data.result.message)
				loadingBar.error()
			}
			buttonLoading[name] = false
		})
		.catch((err) => {
			message.error("Failed to suspend" + name)
			console.log(err)
			buttonLoading[name] = false
			loadingBar.error()
		})
}

function confirmResume(name) {
	loadingBar.start()
	buttonLoading[name] = true
	resumeVm(name)
		.then((res) => {
			if (res.data.result.success) {
				message.success("Resume successful " + name)
				loadingBar.finish()
				state.refreshState()
			} else {
				message.error(res.data.result.message)
				loadingBar.error()
			}
			buttonLoading[name] = false
		})
		.catch((err) => {
			message.error("Failed to suspend" + name)
			console.log(err)
			buttonLoading[name] = false
			loadingBar.error()
		})
}

function confirmDestroy(name) {
	loadingBar.start()
	buttonLoading[name] = true
	destroyVm(name)
		.then((res) => {
			if (res.data.result.success) {
				message.success("Destroyed successfully " + name)
				loadingBar.finish()
				state.refreshState()
			} else {
				message.error(res.data.result.message)
				loadingBar.error()
			}
			buttonLoading[name] = false
		})
		.catch((err) => {
			message.error("Failed to shutdown " + name)
			console.log(err)
			buttonLoading[name] = false
			loadingBar.error()
		})
}
</script>
<template>
	<n-thing content-indented>
		<template #avatar>
			<n-icon size="1.5rem">
				<Desktop />
			</n-icon>
		</template>
		<template #header>
			<div style="font-size: 14px">{{ vm.name }}</div>
		</template>
		<template #header-extra>
			<n-button
				v-if="vm.state === 'shutoff'"
				tertiary
				round
				style="float: right"
				type="primary"
				:loading="buttonLoading[vm.name]"
				@click="handleVmStart(vm.name)"
			>
				<template #icon>
					<PowerOff />
				</template>
			</n-button>
			<n-popconfirm
				v-else-if="vm.state !== 'paused'"
				@positive-click="confirmShutdown(vm.name)"
			>
				<template #trigger>
					<n-button tertiary round type="warning" :loading="buttonLoading[vm.name]">
						<template #icon>
							<PowerOff />
						</template>
					</n-button>
				</template>
				Shutdown {{ vm.name }}?
			</n-popconfirm>
			<n-popconfirm
				v-else-if="vm.state === 'paused'"
				@positive-click="confirmResume(vm.name)"
			>
				<template #trigger>
					<n-button tertiary round type="info" :loading="buttonLoading[vm.name]">
						<template #icon>
							<RefreshOutlined />
						</template>
					</n-button>
				</template>
				Resume {{ vm.name }}?
			</n-popconfirm>
		</template>
		<template v-if="vm.state !== 'shutoff'" #description>
			<span style="float: left; font-size: 12px">
				{{ vm.state }}
			</span>
		</template>
		<template v-if="vm.state !== 'shutoff'" #action>
			<n-space justify="end">
				<n-popconfirm
					v-if="vm.state !== 'paused'"
					@positive-click="confirmSuspend(vm.name)"
				>
					<template #trigger>
						<n-button tertiary round type="info" :loading="buttonLoading[vm.name]">
							<template #icon>
								<Pause />
							</template>
						</n-button>
					</template>
					Suspend {{ vm.name }}?
				</n-popconfirm>
				<n-popconfirm @positive-click="confirmDestroy(vm.name)">
					<template #trigger>
						<n-button tertiary round type="error" :loading="buttonLoading[vm.name]">
							<template #icon>
								<Skull />
							</template>
						</n-button>
					</template>
					Destroy {{ vm.name }}!?
				</n-popconfirm>
			</n-space>
		</template>
		<template v-if="vm.mem_modifiable && vm.state !== 'shutoff'">
			<br />
			<n-space v-if="windowWidth <= 720" style="align-items: center"
				>MEMORY:
				<MemoryDropdown :vm="vm" />
			</n-space>
			<n-thing v-else>
				<template #header>MEMORY</template>
				<MemorySlider :vm="vm" />
			</n-thing>
		</template>
	</n-thing>
</template>

<style scoped></style>
