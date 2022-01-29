<script setup>
import { inject } from 'vue';
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
import Pause from "../assets/Pause.svg";
import RefreshOutlined from "../assets/RefreshOutlined.svg";
import { PowerOff, Skull } from "@vicons/fa";
import { destroyVm, resumeVm, setVmMemory, startVm, stopVm, suspendVm } from '../utils/api';

const message = useMessage();
const loadingBar = useLoadingBar();
const windowWidth = inject('windowWidth')

const state = inject('state');
let expandedItems = $ref({})
let buttonLoading = $ref({})

const expandHandler = ({ name, expanded }) => expandedItems[name] = expanded

function handleVmStart(name) {
    loadingBar.start();
    buttonLoading[name] = true;
    startVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Successfully started " + name);
            loadingBar.finish();
            state.refreshState()
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
        buttonLoading[name] = false;
    }).catch(
        err => {
            message.error("Failed to start " + name);
            loadingBar.error()
            buttonLoading[name] = false;
            console.log(err);
        }
    );
}

function handleMemoryEdit(name, value) {
    setVmMemory(name, value * 1024 * 1024).then(res => {
        if (res.data.result.success) {
            let index = state.vms.findIndex((vm) => vm.name === name)
            state.vms[index].current_memory = value * 1024 * 1024;
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


function confirmShutdown(name) {
    loadingBar.start();
    buttonLoading[name] = true;
    stopVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Shutdown successful " + name);
            loadingBar.finish();
            state.refreshState()
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
        buttonLoading[name] = false;
    }).catch(
        err => {
            message.error("Failed to shutdown " + name);
            console.log(err);
            buttonLoading[name] = false;
            loadingBar.error()
        }
    );
}

function confirmSuspend(name) {
    loadingBar.start();
    buttonLoading[name] = true;
    suspendVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Suspending successful " + name);
            loadingBar.finish();
            state.refreshState()
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
        buttonLoading[name] = false;
    }).catch(
        err => {
            message.error("Failed to suspend" + name);
            console.log(err);
            buttonLoading[name] = false;
            loadingBar.error()
        }
    );
}

function confirmResume(name) {
    loadingBar.start();
    buttonLoading[name] = true;
    resumeVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Resume successful " + name);
            loadingBar.finish();
            state.refreshState()
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
        buttonLoading[name] = false;
    }).catch(
        err => {
            message.error("Failed to suspend" + name);
            console.log(err);
            buttonLoading[name] = false;
            loadingBar.error()
        }
    );
}

function confirmDestroy(name) {
    loadingBar.start();
    buttonLoading[name] = true;
    destroyVm(name).then(res => {
        if (res.data.result.success) {
            message.success("Destroyed successfully " + name);
            loadingBar.finish();
            state.refreshState()
        } else {
            message.error(res.data.result.message);
            loadingBar.error()
        }
        buttonLoading[name] = false;
    }).catch(
        err => {
            message.error("Failed to shutdown " + name);
            console.log(err);
            buttonLoading[name] = false;
            loadingBar.error()
        }
    );
}
</script>
<template>
    <n-divider title-placement="left">KVM</n-divider>
    <n-table :striped="true">
        <n-tbody>
            <n-tr v-for="vm in state.vms" :key="vm.name">
                <n-td>
                    <n-collapse @item-header-click="expandHandler" v-if="vm.state !== 'shutoff'">
                        <n-collapse-item :title="vm.name.toUpperCase()" :key="vm.name" :name="vm.name">
                            <n-space v-if="vm.mem_modifiable" :vertical="windowWidth<=720" style="width: max-content;">
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
                    <n-button v-if="vm.state === 'shutoff'" tertiary circle size="large" style="float: right;"
                              type="primary"
                              :loading="buttonLoading[vm.name]" @click="handleVmStart(vm.name)">
                        <template #icon>
                            <PowerOff/>
                        </template>
                    </n-button>
                    <template v-else>
                        <n-space :vertical="windowWidth <= 720" style="float: right;">
                            <n-popconfirm v-if="expandedItems[vm.name] && vm.state !== 'paused'"
                                          @positive-click="confirmSuspend(vm.name)">
                                <template #trigger>
                                    <n-button tertiary circle size="large" type="info"
                                              :loading="buttonLoading[vm.name]">
                                        <template #icon>
                                            <Pause/>
                                        </template>
                                    </n-button>
                                </template>
                                Suspend {{ vm.name }}?
                            </n-popconfirm>
                            <n-popconfirm v-if="vm.state === 'paused'"
                                          @positive-click="confirmResume(vm.name)">
                                <template #trigger>
                                    <n-button tertiary circle size="large" type="info"
                                              :loading="buttonLoading[vm.name]">
                                        <template #icon>
                                            <RefreshOutlined/>
                                        </template>
                                    </n-button>
                                </template>
                                Resume {{ vm.name }}?
                            </n-popconfirm>
                            <n-popconfirm v-if="vm.state !== 'paused'"
                                          @positive-click="confirmShutdown(vm.name)">
                                <template #trigger>
                                    <n-button tertiary circle size="large" type="warning"
                                              :loading="buttonLoading[vm.name]">
                                        <template #icon>
                                            <PowerOff/>
                                        </template>
                                    </n-button>
                                </template>
                                Shutdown {{ vm.name }}?
                            </n-popconfirm>
                            <n-popconfirm v-if="expandedItems[vm.name]" @positive-click="confirmDestroy(vm.name)">
                                <template #trigger>
                                    <n-button tertiary circle size="large" type="error"
                                              :loading="buttonLoading[vm.name]">
                                        <template #icon>
                                            <Skull/>
                                        </template>
                                    </n-button>
                                </template>
                                Destroy {{ vm.name }}!?
                            </n-popconfirm>
                        </n-space>
                    </template>
                </n-td>
            </n-tr>
        </n-tbody>
    </n-table>
</template>

<style>
</style>