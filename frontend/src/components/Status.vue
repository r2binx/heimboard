<script setup>
import { useMessage, NButton, NSpace, NCollapse, NCollapseItem, NIcon, NPopconfirm, NTable, NTbody, NTr, NTd } from "naive-ui";
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

function timeToString(time) {
    if (time < 120) {
        return time + "s";
    } else if (time < 3600) {
        return Math.floor(time / 60) + "m " + time % 60 + "s";
    } else if (time < 86400) {
        return Math.floor(time / 3600) + "h " + Math.floor(time % 3600 / 60) + "m " + time % 60 + "s";
    }
    else {
        return Math.floor(time / 86400) + "d " + Math.floor(time % 86400 / 3600) + "h " + Math.floor(time % 3600 / 60) + "m " + time % 60 + "s";
    }
}

</script>

<template>
    <n-collapse>
        <n-collapse-item style="font-size: xx-large !important;" title="STATUS">
            <template #header-extra>
                <p v-if="state.reachable.value" class="active">ONLINE</p>
                <p v-else class="idle">OFFLINE</p>
            </template>
            <n-table striped v-if="auth.hasPermission('guest')">
                <n-tbody>
                    <n-tr>
                        <n-td>External IPv4</n-td>
                        <n-td>
                            <div style="float: right;">{{ state.fritz.value.ip.v4 }}</div>
                        </n-td>
                    </n-tr>
                    <n-tr>
                        <n-td>UPTIME</n-td>
                        <n-td>
                            <div style="float:right">{{ timeToString(state.uptime.value) }}</div>
                        </n-td>
                    </n-tr>
                    <n-tr v-if="auth.hasPermission('admin')">
                        <n-td>
                            <n-popconfirm @positive-click="rebootConfirm">
                                <template #trigger>
                                    <n-button type="warning">
                                        <template #icon>
                                            <n-icon>
                                                <spinner />
                                            </n-icon>
                                        </template>
                                        REBOOT
                                    </n-button>
                                </template>
                                <div v-if="state.idle.value">Are you sure you want to reboot?</div>
                                <div v-else>System is active, are you sure?</div>
                            </n-popconfirm>
                        </n-td>
                        <n-td>
                            <n-popconfirm @positive-click="shutdownConfirm">
                                <template #trigger>
                                    <n-button style="float: right;" type="error">
                                        <template #icon>
                                            <n-icon>
                                                <power-off />
                                            </n-icon>
                                        </template>SHUTDOWN
                                    </n-button>
                                </template>
                                <div v-if="state.idle.value">Are you sure you want to shutdown?</div>
                                <div v-else>System is active, are you sure?</div>
                            </n-popconfirm>
                        </n-td>
                    </n-tr>
                </n-tbody>
            </n-table>

            <div v-else style="font-size: small;">NOTHING TO SEE HERE...</div>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
</style>

