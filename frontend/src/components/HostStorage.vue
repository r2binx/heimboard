<script setup lang="ts">
import { NDivider, NIcon, NList, NListItem, NProgress, NThing } from "naive-ui";
import { Save } from "@vicons/fa";
import { formatBytes, progressColor } from "@/utils/common";
import useApi from "@/composables/useApi";

const { useApiState } = useApi();
const state = useApiState();
</script>

<template>
    <n-divider title-placement="left">Storage</n-divider>
    <n-list bordered>
        <n-list-item v-for="(mount, index) in state.storage.value" :key="index">
            <n-thing content-indented>
                <template #avatar>
                    <n-icon size="1.5rem" :component="Save" />
                </template>
                <template #header>
                    <div style="font-size: 14px">{{ mount.name }}</div>
                </template>
                <template #description>
                    <span style="float: left; font-size: 12px">
                        {{ formatBytes(mount.usage.free, 1) }} of
                        {{ formatBytes(mount.usage.total, 1) }} left
                    </span>
                </template>
                <br />
                <n-progress
                    type="line"
                    :percentage="mount.usage.percent"
                    :color="progressColor(mount.usage.percent)"
                    :rail-color="progressColor(mount.usage.percent, '33')"
                    :show-indicator="false"
                    :height="16"
                />
            </n-thing>
        </n-list-item>
    </n-list>
</template>
