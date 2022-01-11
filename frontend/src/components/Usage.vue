<script setup>
import { ref, inject, watchEffect, watch } from 'vue'
import { NDivider, NSpace } from 'naive-ui'
import ProgressCircle from "./ProgressCircle.vue";

const auth = inject("auth");
const state = inject("state");

const cpuUsage = ref(0);
const memUsage = ref(0);

const upRate = ref(0)
const netOutPct = ref(0)

const downRate = ref(0)
const netInPct = ref(0)

const bandwidth = ref({})

let usage_connection = null;
let net_connection = null;


watchEffect(async () => {
    if (usage_connection) {
        usage_connection.close();
        usage_connection = null;
    }
    if (net_connection) {
        net_connection.close();
        net_connection = null;
    }

    if (auth.isAuthenticated.value) {
        usage_connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await auth.getToken());
        usage_connection.onmessage = function (event) {
            let data = JSON.parse(event.data)
            cpuUsage.value = data["cpu"];
            memUsage.value = data["memory"]["used"];
        }

        usage_connection.onopen = function () {
            console.log("Successfully connected to the system websocket server...")
        }

        net_connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/net?rate=1&token=' + await auth.getToken());
        net_connection.onmessage = function (event) {
            let data = JSON.parse(event.data);
            downRate.value = ~~(data["in"] / 125000);
            upRate.value = ~~(data["out"] / 125000);

            netOutPct.value = (upRate.value / bandwidth.value.out * 100);
            netInPct.value = (downRate.value / bandwidth.value.in * 100);

        }

        net_connection.onopen = function () {
            console.log("Successfully connected to the fritz websocket server...")
        }
    }
});

watch(() => state.fritz.value, (fritz, prevFritzInfo) => {
    if (fritz) {
        bandwidth.value = {"in": ~~(fritz.net.down / 1e6), "out": ~~(fritz.net.up / 1e6)};
    }
});

</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>
    <n-space vertical>
        <n-space justify="space-around" style="flex-flow: inherit; margin-bottom: 3ex;">
            <progress-circle :percentage="netOutPct" title="UP">
                {{ upRate }}Mbit/s
            </progress-circle>
            <progress-circle :percentage="netInPct" title="DOWN">
                {{ downRate }}Mbit/s
            </progress-circle>
        </n-space>
        <n-space justify="space-around" style="flex-flow: inherit;">
            <progress-circle :percentage="cpuUsage" title="CPU">
                {{ ~~cpuUsage }}%
            </progress-circle>
            <progress-circle :percentage="memUsage" title="MEMORY">
                {{ ~~memUsage }}%
            </progress-circle>
        </n-space>
    </n-space>
</template>

<style>
</style>