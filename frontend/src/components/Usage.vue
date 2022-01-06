<script setup>
import { ref, inject, watchEffect } from 'vue'
import { NDivider, NSpace, NProgress } from 'naive-ui'
import RealtimeChart from './realtimeChart.vue'

const cpuUsage = ref(0);
const memUsage = ref(0);

let old_tx = ref(null);
const net_tx = ref(0);


const cpuData = ref([])

const memData = ref([])

const netOut = ref([])

const auth = inject("auth");
let connection = null;
watchEffect(async () => {
    if (connection) {
        connection.close();
        connection = null;
    }
    if (auth.isAuthenticated.value) {
        connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await auth.getToken());
        connection.onmessage = function (event) {
            let data = JSON.parse(event.data)
            cpuUsage.value = data["cpu"];
            cpuData.value.push([Date.now(), cpuUsage.value]);

            memUsage.value = data["memory"]["used"];
            memData.value.push([Date.now(), memUsage.value]);
            if (old_tx) {
                net_tx.value = ~~((data["net"]["out"] - old_tx.value) / 1024 / 1024 * 8);
            }

            if (net_tx.value < 50) { netOut.value.push([Date.now(), net_tx.value]) }
            old_tx.value = data["net"]["out"];

        }

        connection.onopen = function () {
            console.log("Successfully connected to the websocket server...")
        }
    }
});

</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>
    <realtime-chart title="CPU usage" :max="100" :data="cpuData" :length="10"></realtime-chart>
    <realtime-chart title="Memory usage" :max="100" :data="memData" :length="100"></realtime-chart>
    <realtime-chart title="Net out" :max="40" :data="netOut" :length="100"></realtime-chart>

    <n-space justify="space-around">
        <n-space justify="center" align="center" :vertical="true">
            <n-progress type="circle" :percentage="cpuUsage" />CPU
        </n-space>
        <n-space justify="center" align="center" :vertical="true">
            <n-progress type="circle" :percentage="memUsage" />MEMORY
        </n-space>
    </n-space>
</template>

<style>
</style>