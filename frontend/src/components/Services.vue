<script setup>
import { ref } from 'vue';
import { NDivider, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { fetchIdle } from '../utils/api';

const idle = ref(Boolean);
const idleServices = ref(Object);

fetchIdle().then(res => {
    idle.value = res.data.result
    idleServices.value = res.data.idle
});

</script>
<template>
    <n-divider title-placement="left">SERVICES</n-divider>
    <n-table v-if="idle" :striped="true">
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
            <n-tr v-for="(state, service) in idleServices " :key="service.name">
                <n-td>{{ service.toUpperCase() }}</n-td>
                <n-td>
                    <div v-if="state" style="float: right;" class="idle">IDLE</div>
                    <div v-else style="float: right" class="active">ACTIVE</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>

<style>
</style>