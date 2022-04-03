<script setup>
import { NSelect, useMessage } from "naive-ui"
import { setVmMemory } from "@/utils/api"
import { inject } from "vue"

const props = defineProps({
	vm: Object,
})

const state = inject("state")
const message = useMessage()

function handleMemoryEdit(name, value) {
	setVmMemory(name, value * 1024 * 1024)
		.then((res) => {
			if (res.data.result.success) {
				let index = state.vms.findIndex((vm) => vm.name === name)
				state.vms[index].current_memory = value * 1024 * 1024
				message.success("Successfully set memory of " + name + " to " + value + "GB")
			} else {
				message.error(res.data.result.message)
			}
		})
		.catch((err) => {
			message.error("Failed to set memory of " + name)
			console.log(err)
		})
}

function vmMemoryOptions(max_memory) {
	let options = []
	for (let i = 1; i <= max_memory; i++) {
		options.push({
			value: i,
			label: i + "GB",
		})
	}
	return options
}
</script>

<template>
	<n-select
		style="width: 100px; min-width: 30%; max-width: 80%"
		:value="vm.current_memory / 1024 / 1024"
		:options="vmMemoryOptions(vm.max_memory / 1024 / 1024)"
		@update:value="($event) => handleMemoryEdit(vm.name, $event)"
	/>
</template>
