<script setup>
import { ref, inject, watchEffect, watch } from 'vue'
import { NDivider, NSpace, } from 'naive-ui'
import RadialBar from './radialBar.vue'

const auth = inject("auth");
const state = inject("state");

const cpuUsage = ref(0);
const memUsage = ref(0);

let old_tx = ref(null);
const net_tx = ref(0);


const cpuData = ref([])

const memData = ref([])

const netOut = ref([])
const netOutPct = ref(0)

const netIn = ref([])
const netInPct = ref(0)

let usage_connection = null;
let net_connection = null;

const bandwidth = ref({})

watchEffect(async () => {
    if (usage_connection) {
        usage_connection.close();
        usage_connection = null;
    }
    if (auth.isAuthenticated.value) {
        usage_connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await auth.getToken());
        usage_connection.onmessage = function (event) {
            let data = JSON.parse(event.data)
            cpuUsage.value = data["cpu"];
            cpuData.value.push([Date.now(), cpuUsage.value]);

            memUsage.value = data["memory"]["used"];
            memData.value.push([Date.now(), memUsage.value]);
            if (old_tx) {
                net_tx.value = ~~((data["net"]["out"] - old_tx.value) / 1024 / 1024 * 8);
            }

            old_tx.value = data["net"]["out"];

        }

        usage_connection.onopen = function () {
            console.log("Successfully connected to the system websocket server...")
        }
    }
});


watchEffect(async () => {
    if (net_connection) {
        net_connection.close();
        net_connection = null;
    }
    if (auth.isAuthenticated.value) {
        net_connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/net?rate=1&token=' + await auth.getToken());
        net_connection.onmessage = function (event) {
            let data = JSON.parse(event.data);
            let downRate = ~~(data["in"] / 125000);
            let upRate = ~~(data["out"] / 125000);

            console.log({ "in": downRate, "out": upRate })
            netOut.value.push([Date.now(), downRate]);
            netIn.value.push([Date.now(), upRate]);

            netOutPct.value = ~~(upRate / bandwidth.value.out * 100);
            netInPct.value = ~~(downRate / bandwidth.value.in * 100);

        }

        net_connection.onopen = function () {
            console.log("Successfully connected to the fritz websocket server...")
        }
    }
});

watch(() => state.fritz.value, (fritz, prevFritzInfo) => {
    if (fritz) {
        bandwidth.value = { "in": ~~(fritz.net.down / 1e6), "out": ~~(fritz.net.up / 1e6) };
    }
});

</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>
    <n-space vertical>
        <n-space justify="space-around" style="flex-flow: inherit;">
            <radial-bar title="Upload" :data="netOutPct" />
            <radial-bar title="Download" :data="netInPct" />
        </n-space>
        <n-space justify="space-around" style="flex-flow: inherit;">
            <radial-bar title="CPU" :data="cpuUsage"></radial-bar>
            <radial-bar title="Memory" :data="memUsage" />
        </n-space>
    </n-space>
</template>

<style>
</style>