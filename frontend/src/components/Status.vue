<script setup>
import {
    NButton,
    NCollapse,
    NCollapseItem,
    NDivider,
    NIcon,
    NPopconfirm,
    NTable,
    NTbody,
    NTd,
    NTr,
    useMessage
} from "naive-ui";
import { PowerOff, Spinner } from "@vicons/fa";
import { reboot, shutdown } from "../utils/api.js";
import { inject } from "@vue/runtime-core";
import BootTimePicker from "./BootTimePicker.vue";
import { onBeforeUnmount } from "vue";

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
    } else {
        return Math.floor(time / 86400) + "d " + Math.floor(time % 86400 / 3600) + "h " + Math.floor(time % 3600 / 60) + "m " + time % 60 + "s";
    }
}

let scheduledBoot = $computed(() => {
    let time = new Date(state.schedule.boot)
    return ("0" + time.getHours()).slice(-2) + ":" + ("0" + time.getMinutes()).slice(-2)
})

let uptimeStr = $computed({get: () => timeToString(state.uptime), set: (val) => timeToString(val)})
const interval = setInterval(() => uptimeStr = state.uptime++, 1000)
onBeforeUnmount(() => clearInterval(interval))

</script>

<template>
    <n-collapse>
        <n-collapse-item style="font-size: xx-large !important;" title="STATUS" name="status">
            <template #header-extra>
                <p v-if="state.reachable" class="active">ONLINE</p>
                <p v-else class="idle">OFFLINE</p>
            </template>
            <n-table striped v-if="auth.hasPermission('guest')">
                <n-tbody>
                    <n-tr>
                        <n-td>External IPv4</n-td>
                        <n-td>
                            <div style="float: right;">{{ state.fritz.ip.v4 }}</div>
                        </n-td>
                    </n-tr>
                    <n-tr>
                        <n-td>UPTIME</n-td>
                        <n-td>
                            <div style="float:right">{{ uptimeStr }}</div>
                        </n-td>
                    </n-tr>
                    <n-tr v-if="state.schedule.boot">
                        <n-td>SCHEDULED BOOT</n-td>
                        <n-td>
                            <div style="float:right">at {{ scheduledBoot }}</div>
                        </n-td>
                    </n-tr>
                    <n-tr v-if="auth.hasPermission('admin')">
                        <n-td>
                            <n-popconfirm @positive-click="rebootConfirm">
                                <template #trigger>
                                    <n-button type="warning">
                                        <template #icon>
                                            <n-icon>
                                                <spinner/>
                                            </n-icon>
                                        </template>
                                        REBOOT
                                    </n-button>
                                </template>
                                <div v-if="state.idle">Are you sure you want to reboot?</div>
                                <div v-else>System is active, are you sure?</div>
                            </n-popconfirm>
                        </n-td>
                        <n-td>
                            <n-popconfirm @positive-click="shutdownConfirm">
                                <template #trigger>
                                    <n-button style="float: right;" type="error">
                                        <template #icon>
                                            <n-icon>
                                                <power-off/>
                                            </n-icon>
                                        </template>
                                        SHUTDOWN
                                    </n-button>
                                </template>
                                <div v-if="state.idle">Are you sure you want to shutdown?</div>
                                <div v-else>System is active, are you sure?</div>
                            </n-popconfirm>
                        </n-td>
                    </n-tr>
                </n-tbody>
            </n-table>
            <div v-if="auth.hasPermission('admin')" style="margin: 1em;">
                <n-divider title-placement="left">SCHEDULE BOOT</n-divider>
                <boot-time-picker/>
            </div>


            <div v-else style="font-size: small;">NOTHING TO SEE HERE...</div>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
</style>

