<script setup>
import { NDivider, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { inject, ref, watch } from 'vue';

const state = inject('state');
const activeServices = ref({});

watch(() => state.services.value, (currentServices, oldServices) => {
    activeServices.value = Object.fromEntries(Object.entries(currentServices).filter(([key, value]) => !value))
});
</script>
<template>
    <n-divider title-placement="left">Services</n-divider>
    <n-table v-if="state.idle.value" :striped="true">
        <n-tbody>
            <n-tr>
                <n-td>System</n-td>
                <n-td>
                    <div style="float: right;" class="idle">Idle</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
    <n-table v-else :striped="true">
        <n-tbody>
            <n-tr v-for="(status, service) in activeServices" :key="service.name">
                <n-td>{{ service }}</n-td>
                <n-td>
                    <div
                        :class="status ? 'idle' : 'active'"
                        style="float: right;"
                    >{{ status ? "Idle" : "Active" }}
                    </div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>