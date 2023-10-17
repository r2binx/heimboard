<script setup lang="ts">
import BootTimePicker from "@/components/BootTimePicker.vue";
import RefreshOutlined from "@/components/icons/RefreshOutlined.vue";
import useApi from "@/composables/useApi";
import useAuth0 from "@/composables/useAuth0";
import { timeToString } from "@/utils/common";
import { PowerOff } from "@vicons/fa";
import {
    NButton,
    NCollapse,
    NCollapseItem,
    NPopconfirm,
    NSpace,
    NTable,
    NTbody,
    NTd,
    NTr,
    useMessage,
} from "naive-ui";
import { computed, onBeforeUnmount } from "vue";

const { hasPermission, isAdmin } = useAuth0();
const message = useMessage();

const { shutdown, tryShutdown, reboot } = useApi();
const { useApiState } = useApi();
const state = useApiState();

function shutdownConfirm() {
    shutdown()
        .then((res) => {
            if (res.data.success) {
                message.success("Shutting down!");
            } else {
                message.error(res.data.message);
            }
        })
        .catch((err) => {
            message.error("Failed to shutdown!");
            console.log(err);
        });
}

function tryShutdownConfirm() {
    console.log("try shutdown click confirmed");
    tryShutdown()
        .then((res) => {
            if (res.data.success) {
                message.success("Shutting down when inactive!");
            } else {
                message.error(res.data.message);
            }
        })
        .catch((err) => {
            message.error("Failed to shutdown!");
            console.log(err);
        });
}

function rebootConfirm() {
    reboot()
        .then((res) => {
            console.log(res.data);
            if (res.data.success) {
                message.success("Rebooted!");
            } else {
                message.error(res.data.message);
            }
        })
        .catch((err) => {
            message.error("Failed to reboot!");
            console.log(err);
        });
}

let uptimeStr = computed<string>(() => timeToString(state.uptime.value));
const interval = setInterval(() => state.uptime.value++, 1000);
onBeforeUnmount(() => clearInterval(interval));
</script>

<template>
    <n-collapse>
        <n-collapse-item class="status-collapse" title="STATUS" name="status">
            <template #header-extra>
                <p v-if="state.reachable.value" class="active">ONLINE</p>
                <p v-else class="idle">OFFLINE</p>
            </template>
            <n-space v-if="hasPermission()" vertical>
                <n-table striped>
                    <n-tbody>
                        <n-tr v-if="state.fritz.value">
                            <n-td>External IPv4</n-td>
                            <n-td>
                                <div style="float: right">
                                    {{ state.fritz.value.ip.v4 }}
                                </div>
                            </n-td>
                        </n-tr>
                        <n-tr>
                            <n-td>UPTIME</n-td>
                            <n-td>
                                <div style="float: right">{{ uptimeStr }}</div>
                            </n-td>
                        </n-tr>
                        <n-tr>
                            <n-td>SCHEDULED BOOT</n-td>
                            <n-td>
                                <boot-time-picker
                                    style="float: right; text-align: center"
                                />
                            </n-td>
                        </n-tr>
                        <n-tr v-if="isAdmin()">
                            <n-td>
                                <n-popconfirm @positive-click="rebootConfirm">
                                    <template #trigger>
                                        <n-button
                                            round
                                            size="large"
                                            tertiary
                                            type="warning"
                                        >
                                            <template #icon>
                                                <RefreshOutlined />
                                            </template>
                                            REBOOT
                                        </n-button>
                                    </template>
                                    <div v-if="state.active.value">
                                        System is active, are you sure?
                                    </div>
                                    <div v-else>Are you sure you want to reboot?</div>
                                </n-popconfirm>
                            </n-td>
                            <n-td>
                                <!-- TODO: implement shutdown when active (wait for inactive) or immediate shutdown -->
                                <n-popconfirm @positive-click="shutdownConfirm">
                                    <template #trigger>
                                        <n-button
                                            round
                                            tertiary
                                            size="large"
                                            style="float: right"
                                            type="error"
                                        >
                                            <template #icon>
                                                <PowerOff />
                                            </template>
                                            SHUTDOWN
                                        </n-button>
                                    </template>
                                    <template v-if="state.active.value" #action>
                                        <n-button
                                            type="error"
                                            size="small"
                                            @click="shutdownConfirm"
                                        >
                                            <template #icon>
                                                <PowerOff />
                                            </template>
                                            NOW
                                        </n-button>
                                        <n-button
                                            type="warning"
                                            size="small"
                                            @click="tryShutdownConfirm"
                                        >
                                            <template #icon>
                                                <PowerOff />
                                            </template>
                                            LATER
                                        </n-button>
                                    </template>
                                    <div v-if="state.active.value">
                                        System is active, are you sure?
                                    </div>
                                    <div v-else>Are you sure you want to shutdown?</div>
                                </n-popconfirm>
                            </n-td>
                        </n-tr>
                    </n-tbody>
                </n-table>
            </n-space>
            <div v-else style="font-size: small">NOTHING TO SEE HERE...</div>
        </n-collapse-item>
    </n-collapse>
</template>

<style>
.status-collapse .n-collapse-item__header * {
    font-size: 16px;
}
</style>
