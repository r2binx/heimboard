<script setup>
import { ref } from 'vue';
import { useMessage, useLoadingBar, NInputNumber, NPopconfirm, NDivider, NSpace, NButton, NCollapse, NCollapseItem, NTable, NTbody, NTr, NTd } from 'naive-ui';
import { fetchAllVms, startVm, stopVm, setVmMemory } from '../utils/api';

const message = useMessage();
const loadingBar = useLoadingBar();
const vmList = ref([]);

function refreshVms() {
    fetchAllVms().then(res => {
        if (res.status == 200) {
            vmList.value = res.data.result;
        }
    }).catch(err => {
        console.log(err);
    });
}

refreshVms();

function handleVmStart(name) {
    loadingBar.start();
    startVm(name).then(res => {
        if (res.data.result.success) {
            let index = vmList.value.findIndex((vm) => vm.name == name)
            vmList.value[index].state = "running";
            message.success("Successfully started " + name);
            loadingBar.finish();
            refreshVms();
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
    }).catch(
        err => {
            message.error("Failed to start " + name);
            loadingBar.error()
            console.log(err);
        }
    );
}

function confirmShutdown(name) {
    loadingBar.start();
    stopVm(name).then(res => {
        if (res.data.result.success) {
            let index = vmList.value.findIndex((vm) => vm.name == name)
            vmList.value[index].state = "shutoff";
            message.success("Shutdown successfull " + name);
            loadingBar.finish();
            refreshVms();
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
    }).catch(
        err => {
            message.error("Failed to shutdown " + name);
            console.log(err);
            loadingBar.error()
        }
    );
}

function handleMemoryEdit(name, value) {
    setVmMemory(name, value * 1024 * 1024).then(res => {
        if (res.data.result.success) {
            let index = vmList.value.findIndex((vm) => vm.name == name)
            vmList.value[index].current_memory = value * 1024 * 1024;
            message.success("Successfully set memory of " + name + " to " + value + "GB");
            refreshVms();
        } else {
            message.error(res.data.result.message);
        }
    }).catch(
        err => {
            message.error("Failed to set memory of " + name);
            console.log(err);
        }
    );
}

</script>
<template>
    <n-divider title-placement="left">KVM</n-divider>
    <n-table :striped="true">
        <n-tbody>
            <n-tr v-for="vm in vmList" :key="vm.name">
                <n-td>
                    <n-collapse v-if="vm.state == 'running' && vm.mem_modifiable">
                        <n-collapse-item :title="vm.name.toUpperCase()" :key="vm.name">
                            <n-space style="width: max-content;">
                                MEMORY:
                                <n-input-number
                                    style="width: 150px; min-width: 30%; max-width: 80%;"
                                    size="small"
                                    :max="vm.max_memory / 1024 / 1024"
                                    :value="vm.current_memory / 1024 / 1024"
                                    @update:value="$event => handleMemoryEdit(vm.name, $event)"
                                />
                            </n-space>
                        </n-collapse-item>
                    </n-collapse>
                    <div v-else>{{ vm.name.toUpperCase() }}</div>
                </n-td>
                <n-td>
                    <n-space style="float: right;" v-if="vm.state == 'running'">
                        <n-popconfirm @positive-click="confirmShutdown(vm.name)">
                            <template #trigger>
                                <n-button type="error">SHUTDOWN</n-button>
                            </template>
                            Shutdown?
                        </n-popconfirm>
                    </n-space>
                    <n-button
                        style="float: right;"
                        type="primary"
                        v-else-if="vm.state == 'shutoff'"
                        @click="handleVmStart(vm.name)"
                    >START</n-button>
                    <div style="float: right;" v-else>{{ vm.sate.toUpperCase() }}</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>

<style>
</style>