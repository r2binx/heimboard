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
    <n-divider title-placement="left">Services</n-divider>
    <n-table v-if="idle" :striped="true">
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
            <n-tr v-for="(state, service) in idleServices " :key="service.name">
                <n-td>{{ service }}</n-td>
                <n-td>
                    <div v-if="state" style="float: right;" class="idle">Idle</div>
                    <div v-else style="float: right" class="active">Idle</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>