<script setup>
import { ref } from 'vue'
import { NDivider, NSpace, NProgress } from 'naive-ui'

const cpuUsage = ref(0);
const memUsage = ref(0);

let connection = new WebSocket('ws://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage/1');
connection.onmessage = function (event) {
    let data = JSON.parse(event.data)
    cpuUsage.value = data["cpu"];
    memUsage.value = data["memory"]["used"];
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