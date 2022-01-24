<script setup>
import { inject, onMounted, onUnmounted } from 'vue';
// import { $ref } from 'vue/macros'
import {
    NButton,
    NCollapse,
    NCollapseItem,
    NDivider,
    NPopconfirm,
    NSelect,
    NSpace,
    NTable,
    NTbody,
    NTd,
    NTr,
    useLoadingBar,
    useMessage
} from 'naive-ui';
import { setVmMemory, startVm, stopVm } from '../utils/api';

const message = useMessage();
const loadingBar = useLoadingBar();
let windowWidth = $ref(window.innerWidth)
const onWidthChange = () => windowWidth = window.innerWidth
onMounted(() => window.addEventListener('resize', onWidthChange))
onUnmounted(() => window.removeEventListener('resize', onWidthChange))

const state = inject('state');

function handleVmStart(name) {
    loadingBar.start();
    startVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Successfully started " + name);
            loadingBar.finish();
            state.refreshState()
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
            message.success("Shutdown successfull " + name);
            loadingBar.finish();
            state.refreshState()
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
            let index = state.vms.value.findIndex((vm) => vm.name === name)
            state.vms.value[index].current_memory = value * 1024 * 1024;
            message.success("Successfully set memory of " + name + " to " + value + "GB");
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

function vmMemoryOptions(max_memory) {
    let options = [];
    for (let i = 1; i <= max_memory; i++) {
        options.push({
            value: i,
            label: i + "GB"
        })
    }
    return options;
}

</script>
<template>
    <n-divider title-placement="left">KVM</n-divider>
    <n-table :striped="true">
        <n-tbody>
            <n-tr v-for="vm in state.vms.value" :key="vm.name">
                <n-td>
                    <n-collapse v-if="vm.state === 'running' && vm.mem_modifiable">
                        <n-collapse-item :title="vm.name.toUpperCase()" :key="vm.name">
                            <n-space
                                :vertical="windowWidth<=720"
                                style="width: max-content;"
                            >
                                MEMORY:
                                <n-select
                                    style="width: 100px; min-width: 30%; max-width: 80%;"
                                    :value="vm.current_memory / 1024 / 1024"
                                    :options="vmMemoryOptions(vm.max_memory / 1024 / 1024)"
                                    @update:value="$event => handleMemoryEdit(vm.name, $event)"
                                />
                            </n-space>
                        </n-collapse-item>
                    </n-collapse>
                    <div v-else>{{ vm.name.toUpperCase() }}</div>
                </n-td>
                <n-td>
                    <n-space style="float: right;" v-if="vm.state === 'running'">
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
                        v-else-if="vm.state === 'shutoff'"
                        @click="handleVmStart(vm.name)"
                    >START
                    </n-button>
                    <div style="float: right;" v-else>{{ vm.state.toUpperCase() }}</div>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>

<style>
</style>