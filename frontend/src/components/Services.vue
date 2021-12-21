<script setup>
import { NDivider, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { state } from '../utils/api.js';

</script>
<template>
    <n-divider title-placement="left">SERVICES</n-divider>
    <n-table v-if="state.idle" :striped="true">
        <n-tbody>
            <n-tr>
                <n-td>SYSTEM</n-td>
                <n-td>
                    <div style="float: right;" class="idle">IDLE</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
    <n-table v-else :striped="true">
        <n-tbody>
            <n-tr v-for="(status, service) in state.services " :key="service.name">
                <n-td>{{ service.toUpperCase() }}</n-td>
                <n-td>
                    <div v-if="status" style="float: right;" class="idle">IDLE</div>
                    <div v-else style="float: right" class="active">ACTIVE</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>

<style>
</style>