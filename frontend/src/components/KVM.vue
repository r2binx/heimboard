<script setup lang="ts">
import { NDivider, NList, NListItem } from "naive-ui";
import KvmThing from "@/components/KvmThing.vue";
import useApi from "@/composables/useApi";

const { useApiState } = useApi();
const state = useApiState();
</script>

<template>
    <n-divider title-placement="left">LIBVIRT</n-divider>
    <template v-if="state.vms">
        <n-list bordered>
            <n-list-item v-for="vm in state.vms.value" :key="vm.name">
                <KvmThing :vm="vm" />
            </n-list-item>
        </n-list>
    </template>
    <p v-else>no vms</p>
</template>

<style></style>
