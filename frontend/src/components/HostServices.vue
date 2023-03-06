<script setup lang="ts">
import useApi from "@/composables/useApi";
import { NDivider, NTable, NTbody, NTd, NTr } from "naive-ui";

const { useApiState } = useApi();
const state = useApiState();
</script>

<template>
    <n-divider title-placement="left">Services</n-divider>
    <n-table v-if="state.active.value" :striped="true">
        <n-tbody>
            <n-tr v-for="(status, service) in state.services.value" :key="service">
                <n-td>{{ service }}</n-td>
                <n-td>
                    <div :class="status ? 'active' : 'idle'" style="float: right">
                        {{ status ? "Active" : "Idle" }}
                    </div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
    <n-table v-else :striped="true">
        <n-tbody>
            <n-tr>
                <n-td>System</n-td>
                <n-td>
                    <div style="float: right" class="idle">Idle</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>
