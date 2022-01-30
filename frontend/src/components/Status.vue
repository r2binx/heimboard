<script setup>
import { NButton, NCollapse, NCollapseItem, NPopconfirm, NSpace, NTable, NTbody, NTd, NTr, useMessage } from "naive-ui";
import { PowerOff } from "@vicons/fa";
import RefreshOutlined from "../assets/RefreshOutlined.svg";
import { reboot, shutdown } from "../utils/api.js";
import BootTimePicker from "./BootTimePicker.vue";
import { inject, onBeforeUnmount } from "vue";
import { timeToString } from "../utils/misc.js";

const props = defineProps({
    scheduledBoot: String,
})
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


let uptimeStr = $computed({ get: () => timeToString(state.uptime), set: (val) => timeToString(val) })
const interval = setInterval(() => uptimeStr = state.uptime++, 1000)
onBeforeUnmount(() => clearInterval(interval))

</script>

<template>
    <n-collapse>
        <n-collapse-item class="status-collapse" title="STATUS" name="status">
            <template #header-extra>
                <p v-if="state.reachable" class="active">ONLINE</p>
                <p v-else class="idle">OFFLINE</p>
            </template>
            <n-space vertical v-if="auth.hasPermission('guest')">
                <n-table striped>
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
                        <n-tr v-if="props.scheduledBoot">
                            <n-td>SCHEDULED BOOT</n-td>
                            <n-td>
                                <div style="float:right">at {{ props.scheduledBoot }}</div>
                            </n-td>
                        </n-tr>
                        <n-tr v-if="auth.hasPermission('admin')">
                            <n-td>
                                <n-popconfirm @positive-click="rebootConfirm">
                                    <template #trigger>
                                        <n-button round size="large" tertiary type="warning">
                                            <template #icon>
                                                <RefreshOutlined/>
                                            </template>
                                            REBOOT
                                        </n-button>
                                    </template>
                                    <div v-if="state.active">System is active, are you sure?</div>
                                    <div v-else>Are you sure you want to reboot?</div>
                                </n-popconfirm>
                            </n-td>
                            <n-td>
                                <n-popconfirm @positive-click="shutdownConfirm">
                                    <template #trigger>
                                        <n-button round tertiary size="large" style="float: right;" type="error">
                                            <template #icon>
                                                <PowerOff/>
                                            </template>
                                            SHUTDOWN
                                        </n-button>
                                    </template>
                                    <div v-if="state.active">System is active, are you sure?</div>
                                    <div v-else>Are you sure you want to shutdown?</div>
                                </n-popconfirm>
                            </n-td>
                        </n-tr>
                    </n-tbody>
                </n-table>
                <n-collapse v-if="auth.hasPermission('admin')">
                    <n-collapse-item
                        title="schedule boot"
                        name="schedule"
                        style="margin: 1em 0 !important"
                    >
                        <boot-time-picker/>
                    </n-collapse-item>
                </n-collapse>
            </n-space>
            <div v-else style="font-size: small;">NOTHING TO SEE HERE...</div>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
.status-collapse .n-collapse-item__header * {
    font-size: 16px;
}
</style>

