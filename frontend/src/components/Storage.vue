<script setup>
import { NDivider, NProgress, NTable, NTbody, NTd, NTr } from 'naive-ui';
import { inject, watchEffect } from 'vue';
import { fetchStorageUsage } from "../utils/api";
import { formatBytes, progressColor } from '../utils/misc.js'

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
    <n-table :striped="true">
        <n-tbody>
            <n-tr v-for="mount in storage" :key="mount.name">
                <n-td style="width: 120px; overflow: hidden">{{ mount.name }}</n-td>
                <n-td>
                    <n-progress type="line" :percentage="mount.usage.percent"
                                :color="progressColor(mount.usage.percent)"
                                :rail-color="progressColor(mount.usage.percent, '33')"
                                :indicator-placement="'inside'" :height="20"
                    >
                        <!-- slot with indicator-placement='inside' currently not supported-->
                        {{ formatBytes(mount.usage.free) }}/{{ formatBytes(mount.usage.total) }}
                    </n-progress>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>