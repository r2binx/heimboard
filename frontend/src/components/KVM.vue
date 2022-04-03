<script setup>
import { inject } from "vue"
// import { $ref } from 'vue/macros'
import { NDivider, NList, NListItem } from "naive-ui"
import KvmThing from "@/components/KvmThing.vue"

const state = inject("state")
</script>
<template>
	<n-divider title-placement="left">LIBVIRT</n-divider>
	<n-list bordered>
		<n-list-item v-for="vm in state.vms" :key="vm.name">
			<KvmThing :vm="vm" />
		</n-list-item>
	</n-list>
</template>

<style></style>
