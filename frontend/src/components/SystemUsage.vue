<script setup>
import { inject, watchEffect } from 'vue'
// import { $computed, $ref } from 'vue/macros'
import { NDivider, NSpace } from 'naive-ui'
import ProgressCircle from "@/components/ProgressCircle.vue";

const auth = inject("auth");

let cpuUsage = $ref(0);
let memUsage = $ref(0);

let usage_connection = null;

watchEffect(async () => {
    if (usage_connection) {
        usage_connection.close();
        usage_connection = null;
    }

    if (auth.isAuthenticated.value) {
        usage_connection = new WebSocket('wss://' + import.meta.env.VITE_APP_IDLEREPORTER + '/usage?rate=1&token=' + await auth.getToken());
        usage_connection.onmessage = function (event) {
            let data = JSON.parse(event.data)
            cpuUsage = data["cpu"];
            memUsage = data["memory"]["used"];
        }

        usage_connection.onopen = function () {
            console.log("Successfully connected to the system websocket server...")
        }

    }
});

</script>
<template>
    <n-divider title-placement="left">SYSTEM</n-divider>
    <n-space justify="space-around">
        <progress-circle :percentage="cpuUsage" title="CPU">
            {{ ~~cpuUsage }}%
        </progress-circle>
        <progress-circle :percentage="memUsage" title="MEMORY">
            {{ ~~memUsage }}%
        </progress-circle>
    </n-space>
</template>

<style>
</style>