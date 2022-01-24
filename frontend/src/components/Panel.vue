<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { inject } from "vue";
import { NSpace, NButton, NIcon, NLoadingBarProvider, NMessageProvider, NResult } from "naive-ui";
import { PowerOff } from "@vicons/fa";
import Status from "./Status.vue";
import Usage from "./Usage.vue";
import Services from "./Services.vue";
import KVM from "./KVM.vue";
import { fetchWakeAvail, wakeOnLan } from "../utils/api.js";

const auth = inject("auth");
const state = inject("state");

function handleWakeUp() {
    wakeOnLan().then(res => {
        if (res.data.success) {
            console.success("Woke up!");
        } else {
            console.error(res.data.message);
        }
    }).catch(
        err => {
            console.error("Failed to wake up!");
            console.log(err);
        }
    );
}

const netReachable = () => {
    fetchWakeAvail().then(res => {
        return res.status === 200
    }).catch(() => {
        return false
    })
}

let scheduledBoot = $computed(() => {
    let time = new Date(state.schedule.boot)
    return ("0" + time.getHours()).slice(-2) + ":" + ("0" + time.getMinutes()).slice(-2)
})

</script>

<template>
    <div>
        <div v-if="state.reachable">
            <n-message-provider>
                <Status/>
            </n-message-provider>
            <Usage/>
            <Services/>
            <n-message-provider v-if="auth.hasPermission('admin')">
                <n-loading-bar-provider>
                    <KVM/>
                </n-loading-bar-provider>
            </n-message-provider>
        </div>
        <div v-else-if="auth.hasPermission('guest')">
            <n-space vertical justify="center" v-if="netReachable">
                <p>Scheduled boot is at: {{ scheduledBoot }} </p>
                <br>
                <n-button @click="handleWakeUp" style="font-size: 72px;" circle :bordered="false">
                    <n-icon>
                        <PowerOff/>
                    </n-icon>
                </n-button>
                <p style="font-size: large;">WAKE UP</p>
            </n-space>
            <n-result v-else status="error" description="Seems like the network is unreachable"></n-result>
        </div>
        <div v-else>
            <p>You haven't been authorized yet to view this page.</p>
        </div>
    </div>
</template>
