<script setup>
import { ref } from 'vue'
import { NDivider, NSpace, NProgress } from 'naive-ui'
import { getToken } from '../utils/useAuth0';

const cpuUsage = ref(0);
const memUsage = ref(0);

let old_tx = ref(null);
const net_tx = ref(0);

let connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await getToken());
connection.onmessage = function (event) {
    let data = JSON.parse(event.data)
    cpuUsage.value = data["cpu"];
    memUsage.value = data["memory"]["used"];
    if (old_tx) {
        net_tx.value = ~~((data["net"]["out"] - old_tx.value) / 1024 / 1024 * 8);
    }

    old_tx.value = data["net"]["out"];
}

connection.onopen = function () {
    console.log("Successfully connected to the websocket server...")
}
</script>
<template>
    <n-divider title-placement="left">USAGE</n-divider>

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