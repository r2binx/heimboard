<script setup>
import { useMessage, NButton, NSpace, NCollapse, NCollapseItem, NIcon, NPopconfirm } from "naive-ui";
import { PowerOff, Spinner } from "@vicons/fa";
import { reboot, shutdown } from "../utils/api.js";
import { inject } from "@vue/runtime-core";

const message = useMessage();

const auth = inject("auth");
const state = inject("state");

function shutdownConfirm() {
    shutdown().then(res => {
        if (res.data.success) {
            message.success("Shutting down!");
        } else {
            message.error(res.data.message);
        }
    }).catch(
        err => {
            message.error("Failed to shutdown!");
            console.log(err);
        }
    );

}

function rebootConfirm() {
    reboot().then(res => {
        console.log(res.data)
        if (res.data.success) {
            message.success("Rebooted!");
        } else {
            message.error(res.data.message);
        }
    }).catch(
        err => {
            message.error("Failed to reboot!");
            console.log(err);
        }
    );

}

</script>

<template>
    <n-collapse>
        <n-collapse-item style="font-size: xx-large !important;" title="STATUS">
            <template #header-extra>
                <p v-if="state.reachable.value" class="active">ONLINE</p>
                <p v-else class="idle">OFFLINE</p>
            </template>
            <n-space v-if="auth.hasPermission('admin')" justify="space-around" size="large">
                <n-popconfirm @positive-click="rebootConfirm">
                    <template #trigger>
                        <n-button type="warning">
                            <template #icon>
                                <n-icon color="#18181c">
                                    <spinner />
                                </n-icon>
                            </template>
                            REBOOT
                        </n-button>
                    </template>
                    <div v-if="state.idle.value">Are you sure you want to reboot?</div>
                    <div v-else>System is active, are you sure?</div>
                </n-popconfirm>
                <n-popconfirm @positive-click="shutdownConfirm">
                    <template #trigger>
                        <n-button type="error">
                            <template #icon>
                                <n-icon color="#18181c">
                                    <power-off />
                                </n-icon>
                            </template>SHUTDOWN
                        </n-button>
                    </template>
                    <div v-if="state.idle.value">Are you sure you want to shutdown?</div>
                    <div v-else>System is active, are you sure?</div>
                </n-popconfirm>
            </n-space>
            <div v-else style="font-size: small;">NOTHING TO SEE HERE...</div>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
</style>

