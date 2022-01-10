<script setup>
import { ref, inject, watchEffect, watch } from 'vue'
import { NDivider, NSpace, NProgress } from 'naive-ui'

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

function circleColor(value, alpha = 'FF') {
    if (value < 25) {
        return '#87D4F9' + alpha;
    } else if (value >= 25 && value < 40) {
        return '#61DBC3' + alpha;
    } else if (value >= 40 && value < 70) {
        return '#95DA74' + alpha;
    } else if (value >= 70 && value < 90) {
        return '#FAD375' + alpha;
    } else {
        return '#D9534F' + alpha;
    }
}
</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>
    <n-space vertical>
        <n-space justify="space-around" style="flex-flow: inherit; margin-bottom: 3ex;">
            <n-progress
                type="circle"
                :color="circleColor(netOutPct)"
                :rail-color="circleColor(netOutPct, '33')"
                :percentage="netOutPct"
            >
                <n-space vertical justify="center">
                    <div style="font-size: x-large">{{ netOutPct }}%</div>
                    <div>UP</div>
                </n-space>
            </n-progress>
            <n-progress
                type="circle"
                :color="circleColor(netInPct)"
                :rail-color="circleColor(netInPct, '33')"
                :percentage="netInPct"
            >
                <n-space vertical justify="center">
                    <div style="font-size: x-large">{{ netInPct }}%</div>
                    <div>DOWN</div>
                </n-space>
            </n-progress>
        </n-space>
        <n-space justify="space-around" style="flex-flow: inherit;">
            <n-progress
                type="circle"
                :color="circleColor(cpuUsage)"
                :rail-color="circleColor(cpuUsage, '33')"
                :percentage="cpuUsage"
            >
                <n-space vertical justify="center">
                    <div style="font-size: x-large">{{ cpuUsage }}%</div>
                    <div>CPU</div>
                </n-space>
            </n-progress>
            <n-progress
                type="circle"
                :color="circleColor(memUsage)"
                :rail-color="circleColor(memUsage, '33')"
                :percentage="memUsage"
            >
                <n-space vertical justify="center">
                    <div style="font-size: x-large">{{ memUsage }}%</div>
                    <div>MEMORY</div>
                </n-space>
            </n-progress>
        </n-space>
    </n-space>
</template>

<style>
</style>