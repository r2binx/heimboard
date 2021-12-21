<script setup>
import { NDivider, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { inject } from 'vue';

const state = inject('state');

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
            <n-tr v-for="(status, service) in state.services.value" :key="service.name">
                <n-td>{{ service }}</n-td>
                <n-td>
                    <div v-if="status" style="float: right;" class="idle">Idle</div>
                    <div v-else style="float: right" class="active">Idle</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>