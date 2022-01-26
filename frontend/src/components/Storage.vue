<script setup>
import { NDivider, NIcon, NList, NListItem, NProgress, NThing } from 'naive-ui';
import { inject, watchEffect } from 'vue';
import { Save } from "@vicons/fa";
import { formatBytes, progressColor } from '../utils/misc.js'
import { fetchStorageUsage } from "../utils/api";

const state = inject('state');

let storage = $ref({})

watchEffect(async () => {
    if (state.reachable) {
        fetchStorageUsage().then(res => {
            if (res.status === 200) {
                storage = res.data.result
            }
        })
    }
})

</script>
<template>
    <n-divider title-placement="left">Storage</n-divider>
    <n-list bordered>
        <n-list-item v-for="(mount, index) in storage" :key="index">
            <n-thing>
                <template #avatar>
                    <n-icon size="1.7rem">
                        <save/>
                    </n-icon>
                </template>
                <template #header>{{ mount.name }}</template>
                <template #description>
                    <span style="float: left">{{ formatBytes(mount.usage.free, 1) }} of {{
                            formatBytes(mount.usage.total, 1)
                        }} left</span>
                </template>
                <n-progress type="line" :percentage="mount.usage.percent"
                            :color="progressColor(mount.usage.percent)"
                            :rail-color="progressColor(mount.usage.percent, '33')"
                            :show-indicator="false" :height="20"/>


            </n-thing>
        </n-list-item>
    </n-list>


</template>