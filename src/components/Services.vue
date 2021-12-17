<script setup>
import { ref } from 'vue';
import { NDivider, NCollapse, NCollapseItem, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { fetchIdle } from '../utils/api';

const activeShade = "#63e2b7";
const idleShade = "#e88080";

const idle = ref(Boolean);
const idleServices = ref(Object);

fetchIdle().then(res => {
    idle.value = res.data.result
    idleServices.value = res.data.idle
});

</script>
<template>
    <n-divider title-placement="left">SERVICES</n-divider>
    <n-collapse :default-expanded-names="() => idle ? null : '1'">
        <n-collapse-item style="font-size: xx-large !important;" title="SYSTEM" name="1">
            <template #header-extra>
                <p v-if="idle" class="idle">IDLE</p>
                <p v-else class="active">ACTIVE</p>
            </template>
            <n-table :striped="true">
                <n-tbody>
                    <n-tr v-for="(state, service) in idleServices " :key="service.name">
                        <n-td>{{ service.toUpperCase() }}</n-td>
                        <n-td>
                            <p v-if="state" style="float: right;" class="idle">IDLE</p>
                            <p v-else style="float: right" class="active">ACTIVE</p>
                        </n-td>
                    </n-tr>
                </n-tbody>
            </n-table>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
.idle {
    color: v-bind(idleShade);
}

.active {
    color: v-bind(activeShade);
}
</style>