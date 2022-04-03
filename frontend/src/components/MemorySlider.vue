<script setup>
import { NSlider, useMessage } from "naive-ui"
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

function vmMemoryMarks(max_memory) {
	let options = {}
	for (let i = 1; i <= max_memory; i++) {
		options[i] = i % 4 === 0 ? i + "GB" : null
	}
	return options
}
</script>

<template>
	<n-slider
		style="width: 90%; margin: 8px auto 42px"
		step="mark"
		:max="props.vm.max_memory / 1024 / 1024"
		:format-tooltip="(value) => `${value}GB`"
		:marks="vmMemoryMarks(props.vm.max_memory / 1024 / 1024)"
		:value="props.vm.current_memory / 1024 / 1024"
		@update:value="($event) => handleMemoryEdit(props.vm.name, $event)"
	/>
</template>

<style scoped></style>
