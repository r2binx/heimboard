<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import {
    NButton,
    NIcon,
    NLoadingBarProvider,
    NMessageProvider,
    NResult,
    NSpace,
    useLoadingBar,
    useMessage,
    type ButtonProps,
} from "naive-ui";
import { PowerOff } from "@vicons/fa";
import HostStatus from "@/components/HostStatus.vue";
import SystemUsage from "@/components/SystemUsage.vue";
import NetworkUsage from "@/components/NetworkUsage.vue";
import HostServices from "@/components/HostServices.vue";
import HostStorage from "@/components/HostStorage.vue";
import BootTimePicker from "@/components/BootTimePicker.vue";
import useApi from "@/composables/useApi";
import useAuth0 from "@/composables/useAuth0";

type ButtonThemeOverrides = NonNullable<ButtonProps["themeOverrides"]>;

const buttonThemeOverrides: ButtonThemeOverrides = {
    iconSizeLarge: "60px",
};

const { hasPermission, isAdmin } = useAuth0();
const { wakeOnLan, useApiState } = useApi();
const state = useApiState();
const loadingBar = useLoadingBar();
const message = useMessage();

const KVM = defineAsyncComponent(() => import("@/components/KVM.vue"));

function handleWakeUp() {
    loadingBar.start();
    wakeOnLan()
        .then((res) => {
            if (res.data.success) {
                loadingBar.finish();
                message.success(
                    "Wake up successful, please wait for services to come online"
                );
                // setTimeout(state.refreshState(accessToken.value), 2000);
            } else {
                console.error(res.data.message);
                loadingBar.error();
                message.error("Wake up failed");
            }
        })
        .catch((err) => {
            loadingBar.error();
            console.error("Failed to wake up!");
            console.log(err);
        });
}
</script>

<template>
    <div v-if="hasPermission()">
        <div v-if="state.reachable.value">
            <n-message-provider>
                <HostStatus />
            </n-message-provider>
            <SystemUsage />
            <NetworkUsage />
            <HostServices v-if="state.active.value" />
            <n-message-provider v-if="isAdmin()">
                <n-loading-bar-provider>
                    <KVM />
                </n-loading-bar-provider>
            </n-message-provider>
            <HostStorage />
        </div>
        <template v-else>
            <n-space v-if="state.net_reachable.value" vertical justify="center">
                <n-space
                    style="margin-bottom: 25px; align-items: center"
                    justify="center"
                >
                    <p>Scheduled boot is at:</p>
                    <BootTimePicker />
                </n-space>
                <n-button
                    :theme-overrides="buttonThemeOverrides"
                    size="large"
                    circle
                    :bordered="false"
                    @click="handleWakeUp"
                >
                    <template #icon>
                        <n-icon>
                            <PowerOff />
                        </n-icon>
                    </template>
                </n-button>
                <p style="font-size: large">WAKE UP</p>
            </n-space>
            <n-result
                v-else
                status="error"
                description="Seems like the network is unreachable"
            ></n-result>
        </template>
    </div>
    <div v-else>
        <p>You haven't been authorized yet to view this page.</p>
    </div>
</template>
